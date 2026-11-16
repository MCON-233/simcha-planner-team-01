"""Contract tests: every ChecklistRepository must pass all of these.

Each test runs once per implementation listed in its fixture's params.
"""
from datetime import date, timedelta

import pytest

from app import create_app
from app.db import db
from app.domain.checklist_item import ChecklistItem
from app.repositories.in_memory_checklist_repo import InMemoryChecklistRepository

READING = ["in_memory", "sqlalchemy"]
CHANGING = ["in_memory", "sqlalchemy"]


def build(kind):
    if kind == "in_memory":
        yield InMemoryChecklistRepository()
        return
    from app.models.event_model import EventModel
    from app.repositories.sqlalchemy_checklist_repository import SqlAlchemyChecklistRepository

    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.app_context():
        # Items point at events, so the events the tests use (ids 1-3) must exist.
        for _ in range(3):
            db.session.add(EventModel(event_type="vort", event_date=date.today() + timedelta(days=30),
                                      guest_count=50, budget=1000))
        db.session.commit()
        yield SqlAlchemyChecklistRepository()
        db.drop_all()


@pytest.fixture(params=READING)
def repo(request):
    yield from build(request.param)


@pytest.fixture(params=CHANGING)
def changing_repo(request):
    yield from build(request.param)


def make_item(event_id=1, title="Book venue", done=False):
    return ChecklistItem(event_id=event_id, title=title, done=done)


# ---- Reading: add, get, for_event ----

def test_add_gives_the_item_an_id(repo):
    saved = repo.add(make_item())

    assert saved.id is not None


def test_each_item_gets_its_own_id(repo):
    first = repo.add(make_item())
    second = repo.add(make_item())

    assert first.id != second.id


def test_get_returns_the_saved_fields(repo):
    saved = repo.add(make_item(event_id=3, title="Send invitations", done=True))

    loaded = repo.get(saved.id)

    assert loaded.id == saved.id
    assert loaded.event_id == 3
    assert loaded.title == "Send invitations"
    assert loaded.done is True


def test_get_returns_none_for_an_unknown_id(repo):
    assert repo.get(999) is None


def test_for_event_is_empty_at_first(repo):
    assert repo.for_event(1) == []


def test_for_event_returns_only_that_events_items(repo):
    repo.add(make_item(event_id=1, title="Book venue"))
    repo.add(make_item(event_id=1, title="Hire photographer"))
    repo.add(make_item(event_id=2, title="Order flowers"))

    titles = sorted(item.title for item in repo.for_event(1))

    assert titles == ["Book venue", "Hire photographer"]


# ---- Changing: update ----

def test_update_is_saved(changing_repo):
    saved = changing_repo.add(make_item(done=False))

    changing_repo.update(saved.id, make_item(done=True))

    assert changing_repo.get(saved.id).done is True


def test_update_keeps_the_id(changing_repo):
    saved = changing_repo.add(make_item())

    changing_repo.update(saved.id, make_item(title="Book hall"))

    assert changing_repo.get(saved.id).id == saved.id


def test_update_returns_the_updated_item(changing_repo):
    saved = changing_repo.add(make_item())

    updated = changing_repo.update(saved.id, make_item(title="Book hall"))

    assert updated.id == saved.id
    assert updated.title == "Book hall"


def test_update_returns_none_for_an_unknown_id(changing_repo):
    assert changing_repo.update(999, make_item()) is None
