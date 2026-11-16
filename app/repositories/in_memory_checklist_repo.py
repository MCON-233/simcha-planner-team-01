from app.domain.checklist_item import ChecklistItem
from app.repositories.checklist_repo import ChecklistRepository

class InMemoryChecklistRepository(ChecklistRepository):
    def __init__(self):
        self._items = {}          # item_id -> ChecklistItem
        self._next_id = 1

    def add(self, item):
        item.id = self._next_id
        self._items[item.id] = item
        self._next_id += 1
        return item

    def get(self, item_id):
        return self._items.get(item_id)

    def for_event(self, event_id):
        return [item for item in self._items.values() if item.event_id == event_id]

    def update(self, item_id, item):
        if item_id not in self._items:
            return None
        item.id = item_id
        self._items[item_id] = item
        return item
