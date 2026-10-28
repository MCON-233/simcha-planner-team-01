from datetime import date, timedelta

import pytest

from app import create_app
from app.domain.event import Event
from app.repositories.database import make_session
from app.repositories.event_repository import SqlAlchemyEventRepository


def future(days=30):
    return date.today() + timedelta(days=days)


@pytest.fixture
def session():
    session = make_session("sqlite://")   # an in-memory SQLite database, gone when the test ends
    yield session
    session.remove()


@pytest.fixture
def repo(session):
    return SqlAlchemyEventRepository(session)


@pytest.fixture
def event():
    return Event("vort", future(), guest_count=80, budget=5000)


def test_add_gives_the_event_an_id(repo, event):
    saved = repo.add(event)

    assert saved.id is not None


def test_get_returns_none_for_an_unknown_id(repo):
    assert repo.get(999) is None


def test_saved_event_comes_back_from_the_database_with_its_details(repo, session, event):
    saved_id = repo.add(event).id
    session.remove()   # throw away the session, so get() must read from the database

    loaded = repo.get(saved_id)

    assert loaded is not event
    assert (loaded.event_type, loaded.event_date, loaded.guest_count, loaded.budget) == \
           ("vort", future(), 80, 5000)
    assert loaded.days_until_event() == 30


def test_all_returns_every_saved_event(repo, event):
    other = Event("bat_mitzvah", future(60), guest_count=40, budget=0)
    repo.add(event)
    repo.add(other)

    assert repo.all() == [event, other]


def test_update_saves_the_new_values(repo, session, event):
    saved_id = repo.add(event).id
    changed = Event("bat_mitzvah", future(60), guest_count=40, budget=0)
    changed.id = saved_id

    repo.update(changed)
    session.remove()

    loaded = repo.get(saved_id)
    assert (loaded.event_type, loaded.event_date, loaded.guest_count, loaded.budget) == \
           ("bat_mitzvah", future(60), 40, 0)
    assert len(repo.all()) == 1


def test_update_returns_none_for_an_unknown_id(repo):
    changed = Event("vort", future(), guest_count=40, budget=0)
    changed.id = 999

    assert repo.update(changed) is None
    assert repo.all() == []


# Production wiring: without TESTING, the app uses the database

def test_app_without_testing_saves_events_in_the_database():
    app = create_app({"DATABASE_URL": "sqlite://", "WTF_CSRF_ENABLED": False})
    client = app.test_client()

    created = client.post("/events", data={"event_type": "vort", "event_date": future(10).isoformat(),
                                           "guest_count": "50", "budget": "1000"})
    page = client.get(created.headers["Location"])
    client.post(created.headers["Location"] + "/edit",
                data={"event_type": "vort", "event_date": future(10).isoformat(),
                      "guest_count": "75", "budget": "1000"})

    assert isinstance(app.extensions["event_service"]._repository, SqlAlchemyEventRepository)
    assert "10 days to go" in page.get_data(as_text=True)
    assert app.extensions["event_service"].list_events()[0].guest_count == 75


def test_testing_app_uses_memory_even_without_a_repository():
    app = create_app({"TESTING": True})

    assert not isinstance(app.extensions["event_service"]._repository, SqlAlchemyEventRepository)
