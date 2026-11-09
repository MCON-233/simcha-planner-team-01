from datetime import date, timedelta

import pytest

from app.domain.event import Event
from app.repositories.in_memory_checklist_repo import InMemoryChecklistRepository
from app.repositories.in_memory_event_repository import InMemoryEventRepository
from app.services.checklist_service import ChecklistService


@pytest.fixture
def events():
    return InMemoryEventRepository()


@pytest.fixture
def items():
    return InMemoryChecklistRepository()


@pytest.fixture
def service(items, events):
    return ChecklistService(items, events)


@pytest.fixture
def event(events):
    return events.add(Event("vort", date.today() + timedelta(days=30), guest_count=50, budget=1000))


# Adding items

def test_add_item_saves_it_for_the_event(service, items, event):
    item = service.add_item(event.id, "Book venue")

    assert items.get(item.id) is item
    assert item.event_id == event.id
    assert item.done is False


def test_add_item_to_an_unknown_event_returns_none(service, items):
    assert service.add_item(999, "Book venue") is None
    assert items.for_event(999) == []


def test_blank_item_is_not_saved(service, items, event):
    with pytest.raises(ValueError):
        service.add_item(event.id, "  ")

    assert items.for_event(event.id) == []


# Listing items

def test_items_for_event_are_in_the_order_they_were_added(service, event):
    service.add_item(event.id, "Book venue")
    service.add_item(event.id, "Send invitations")

    assert [item.title for item in service.items_for_event(event.id)] == ["Book venue", "Send invitations"]


def test_items_for_event_leaves_out_other_events(service, events, event):
    other = events.add(Event("vort", date.today() + timedelta(days=60), guest_count=10, budget=0))
    service.add_item(other.id, "Order flowers")

    assert service.items_for_event(event.id) == []


def test_items_for_an_unknown_event_is_none(service):
    assert service.items_for_event(999) is None


# Ticking items off

def test_toggle_marks_an_item_done_and_back(service, items, event):
    item = service.add_item(event.id, "Book venue")

    service.toggle_item(event.id, item.id)
    assert items.get(item.id).done is True

    service.toggle_item(event.id, item.id)
    assert items.get(item.id).done is False


def test_toggle_returns_the_item(service, event):
    item = service.add_item(event.id, "Book venue")

    assert service.toggle_item(event.id, item.id).id == item.id


def test_toggle_an_unknown_item_returns_none(service, event):
    assert service.toggle_item(event.id, 999) is None


def test_toggle_an_item_of_another_event_returns_none(service, events, items, event):
    other = events.add(Event("vort", date.today() + timedelta(days=60), guest_count=10, budget=0))
    item = service.add_item(other.id, "Order flowers")

    assert service.toggle_item(event.id, item.id) is None
    assert items.get(item.id).done is False
