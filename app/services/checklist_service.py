from app.domain.checklist_item import ChecklistItem
from app.repositories.checklist_repo import ChecklistRepository
from app.repositories.event_repository import EventRepository


class ChecklistService:
    def __init__(self, items: ChecklistRepository, events: EventRepository):
        self._items = items
        self._events = events

    def items_for_event(self, event_id):
        """The event's items in the order they were added, or None if there is no such event."""
        if self._events.get(event_id) is None:
            return None
        return sorted(self._items.for_event(event_id), key=lambda item: item.id)

    def add_item(self, event_id, title):
        """Save a new item for the event, or return None if there is no such event. Raises ValueError for a bad title."""
        if self._events.get(event_id) is None:
            return None
        item = ChecklistItem(event_id, title)   # rules: the ChecklistItem's job
        return self._items.add(item)            # storage: the repository's job

    def toggle_item(self, event_id, item_id):
        """Flip the item between done and not done. None if the event has no such item."""
        item = self._items.get(item_id)
        if item is None or item.event_id != event_id:
            return None
        toggled = ChecklistItem.restore(item.id, item.event_id, item.title, not item.done)
        return self._items.update(item_id, toggled)
