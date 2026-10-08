from datetime import date

from app.domain.event import Event
from app.repositories.event_repository import InMemoryEventRepository


class EventService:
    def __init__(self, repository: InMemoryEventRepository) -> None:
        self._repository = repository

    def create_event(
        self,
        event_type: str,
        event_date: date,
        guest_count: int,
        budget: float,
        venue: str = "",
        theme: str = "",
    ) -> Event:
        event = Event(event_type, event_date, guest_count, budget, venue=venue, theme=theme)
        return self._repository.add(event)

    def get_event(self, event_id: int) -> Event | None:
        return self._repository.get(event_id)
