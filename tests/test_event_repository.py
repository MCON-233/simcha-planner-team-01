from datetime import date, timedelta

import pytest

from app.domain.event import Event
from app.repositories.event_repository import EventRepository
from app.repositories.in_memory_event_repository import InMemoryEventRepository


@pytest.fixture
def repo():
    return InMemoryEventRepository()


@pytest.fixture
def event():
    return Event("vort", date.today() + timedelta(days=30), guest_count=80, budget=5000)


def test_add_gives_the_event_an_id(repo, event):
    saved = repo.add(event)

    assert saved.id is not None


def test_get_returns_the_saved_event(repo, event):
    saved = repo.add(event)

    assert repo.get(saved.id) is saved


def test_get_returns_none_for_an_unknown_id(repo):
    assert repo.get(999) is None


def test_all_returns_every_saved_event(repo, event):
    other = Event("bat_mitzvah", date.today() + timedelta(days=60), guest_count=40, budget=0)
    repo.add(event)
    repo.add(other)

    assert repo.all() == [event, other]


def test_a_repository_must_implement_every_method():
    class Incomplete(EventRepository):
        def add(self, event):
            return event

    with pytest.raises(TypeError):
        Incomplete()


def test_update_replaces_the_saved_event(repo, event):
    saved = repo.add(event)
    changed = Event("bat_mitzvah", date.today() + timedelta(days=60), guest_count=40, budget=0)

    repo.update(saved.id, changed)

    assert repo.get(saved.id) is changed
    assert changed.id == saved.id
    assert repo.all() == [changed]


def test_update_returns_none_for_an_unknown_id(repo, event):
    assert repo.update(999, event) is None
    assert repo.all() == []
