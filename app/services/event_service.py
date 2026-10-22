from app.domain.event import Event
from app.repositories.event_repository import EventRepository


class EventService:
    def __init__(self, repository: EventRepository):
        self._repository = repository

    def create_event(self, event_type, event_date, guest_count, budget):
        event = Event(event_type, event_date, guest_count, budget)   # rules: the Event's job
        return self._repository.add(event)                           # storage: the repository's job

    def get_event(self, event_id):
        return self._repository.get(event_id)

    def list_events(self):
        return sorted(self._repository.all(), key=lambda event: event.event_date)

    def update_event(self, event_id, event_type, event_date, guest_count, budget):
        if self.get_event(event_id) is None:
            return None
        event = Event(event_type, event_date, guest_count, budget)   # rules: the Event's job
        event.id = event_id
        return self._repository.update(event)

