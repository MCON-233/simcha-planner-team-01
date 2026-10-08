from datetime import date, timedelta

import pytest

from app.repositories.event_repository import InMemoryEventRepository
from app.services.event_service import EventService


def future(days: int = 30) -> date:
    return date.today() + timedelta(days=days)


def test_create_event_saves_it() -> None:
    repo = InMemoryEventRepository()
    service = EventService(repo)

    event = service.create_event("bat_mitzvah", future(), guest_count=75, budget=4000)

    assert event.id is not None
    assert repo.get(event.id) is event


def test_invalid_event_is_not_saved() -> None:
    repo = InMemoryEventRepository()
    service = EventService(repo)

    with pytest.raises(ValueError):
        service.create_event("bat_mitzvah", future(), guest_count=0, budget=4000)

    assert repo.all() == []


def test_get_event_returns_none_for_unknown_id() -> None:
    service = EventService(InMemoryEventRepository())

    assert service.get_event(999) is None
