from abc import ABC, abstractmethod
from app.domain.checklist_item import ChecklistItem
class ChecklistRepository(ABC):
    @abstractmethod
    def add(self, item):
        pass

    @abstractmethod
    def get(self, item_id) -> ChecklistItem | None:
        pass

    @abstractmethod
    def for_event(self, event_id) -> list[ChecklistItem]:
        pass

    @abstractmethod
    def update(self, item_id, item) -> ChecklistItem | None:
        pass