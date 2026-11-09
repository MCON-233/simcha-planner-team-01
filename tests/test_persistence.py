from datetime import date, timedelta

from app import create_app


def test_events_survive_a_restart(tmp_path):
    database = f"sqlite:///{tmp_path / 'simcha.db'}"

    first_run = create_app({"SQLALCHEMY_DATABASE_URI": database})
    with first_run.app_context():
        service = first_run.extensions["event_service"]
        service.create_event("vort", date.today() + timedelta(days=30), 80, 5000)

    second_run = create_app({"SQLALCHEMY_DATABASE_URI": database})
    with second_run.app_context():
        events = second_run.extensions["event_service"].list_events()
        assert len(events) == 1
        assert events[0].guest_count == 80


def test_updates_survive_a_restart(tmp_path):
    database = f"sqlite:///{tmp_path / 'simcha.db'}"
    event_date = date.today() + timedelta(days=30)

    first_run = create_app({"SQLALCHEMY_DATABASE_URI": database})
    with first_run.app_context():
        service = first_run.extensions["event_service"]
        event = service.create_event("vort", event_date, 80, 5000)
        service.update_event(event.id, "vort", event_date, 120, 5000)

    second_run = create_app({"SQLALCHEMY_DATABASE_URI": database})
    with second_run.app_context():
        assert second_run.extensions["event_service"].get_event(event.id).guest_count == 120


def test_saved_events_still_load_after_their_date_passes(tmp_path):
    from app.db import db
    from app.models.event_model import EventModel

    app = create_app({"SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmp_path / 'simcha.db'}"})
    with app.app_context():
        row = EventModel(event_type="vort", event_date=date.today() - timedelta(days=3),
                         guest_count=80, budget=5000)
        db.session.add(row)
        db.session.commit()

        service = app.extensions["event_service"]
        assert service.get_event(row.id).event_date == date.today() - timedelta(days=3)
        assert len(service.list_events()) == 1
