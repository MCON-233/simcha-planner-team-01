from datetime import date, timedelta

import pytest

from app.repositories.event_repository import InMemoryEventRepository
from app.services.event_service import EventService


def future(days=30):
    return date.today() + timedelta(days=days)


@pytest.fixture
def repo():
    return InMemoryEventRepository()


@pytest.fixture
def service(repo):
    return EventService(repo)


def test_create_event_saves_it(service, repo):
    event = service.create_event("bat_mitzvah", future(), guest_count=75, budget=4000)

    assert repo.get(event.id) is event


def test_invalid_event_is_not_saved(service, repo):
    with pytest.raises(ValueError):
        service.create_event("bat_mitzvah", future(), guest_count=0, budget=4000)

    assert repo.all() == []


def test_get_event_returns_none_for_an_unknown_id(service):
    assert service.get_event(999) is None


def test_list_events_is_empty_at_first(service):
    assert service.list_events() == []


def test_list_events_returns_soonest_first(service):
    later = service.create_event("vort", future(60), guest_count=50, budget=1000)
    sooner = service.create_event("bar_mitzvah", future(10), guest_count=50, budget=1000)

    assert service.list_events() == [sooner, later]


def test_update_event_saves_the_new_values(service):
    event = service.create_event("vort", future(), guest_count=50, budget=1000)

    updated = service.update_event(event.id, "bar_mitzvah", future(20), guest_count=80, budget=2000)

    assert service.get_event(event.id) is updated
    assert updated.event_type == "bar_mitzvah"
    assert updated.guest_count == 80


def test_invalid_update_leaves_the_event_unchanged(service):
    event = service.create_event("vort", future(), guest_count=50, budget=1000)

    with pytest.raises(ValueError):
        service.update_event(event.id, "vort", future(), guest_count=0, budget=1000)

    assert service.get_event(event.id).guest_count == 50


def test_update_event_returns_none_for_an_unknown_id(service):
    assert service.update_event(999, "vort", future(), guest_count=50, budget=1000) is None


def test_events_on_the_same_date_are_both_listed(service):
    first = service.create_event("vort", future(10), guest_count=50, budget=1000)
    second = service.create_event("bar_mitzvah", future(10), guest_count=50, budget=1000)

    assert service.list_events() == [first, second]
