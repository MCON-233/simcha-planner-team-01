"""Contract tests: every EventRepository must pass all of these.

Each test runs once per implementation listed in its fixture's params.
"""
from datetime import date, timedelta

import pytest

from app import create_app
from app.db import db
from app.domain.event import Event
from app.repositories.in_memory_event_repository import InMemoryEventRepository

READING = ["in_memory", "sqlalchemy"]    # Subtask 3 adds "sqlalchemy"
CHANGING = ["in_memory"]   # Subtask 4 adds "sqlalchemy"


def build(kind):
    if kind == "in_memory":
        yield InMemoryEventRepository()
        return
    from app.repositories.sqlalchemy_event_repository import SqlAlchemyEventRepository

    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.app_context():
        yield SqlAlchemyEventRepository()
        db.drop_all()


@pytest.fixture(params=READING)
def repo(request):
    yield from build(request.param)


@pytest.fixture(params=CHANGING)
def changing_repo(request):
    yield from build(request.param)


def make_event(guest_count=80):
    return Event("vort", date.today() + timedelta(days=30), guest_count=guest_count, budget=5000)


# ---- Reading: add, get, all ----

def test_add_gives_the_event_an_id(repo):
    saved = repo.add(make_event())

    assert saved.id is not None


def test_get_returns_the_saved_fields(repo):
    saved = repo.add(make_event(guest_count=80))

    loaded = repo.get(saved.id)

    assert loaded.id == saved.id
    assert loaded.event_type == "vort"
    assert loaded.guest_count == 80


def test_get_returns_none_for_an_unknown_id(repo):
    assert repo.get(999) is None


def test_all_is_empty_at_first(repo):
    assert repo.all() == []


def test_all_returns_every_saved_event(repo):
    repo.add(make_event())
    repo.add(make_event())

    assert len(repo.all()) == 2


# ---- Changing: update ----

def test_update_is_saved(changing_repo):
    saved = changing_repo.add(make_event(guest_count=80))

    changing_repo.update(saved.id, make_event(guest_count=120))

    assert changing_repo.get(saved.id).guest_count == 120


def test_update_keeps_the_id(changing_repo):
    saved = changing_repo.add(make_event())

    changing_repo.update(saved.id, make_event(guest_count=120))

    assert changing_repo.get(saved.id).id == saved.id
