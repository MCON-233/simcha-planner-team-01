from app.repositories.event_repository import EventRepository


class InMemoryEventRepository(EventRepository):
    """Keeps events in a dictionary. Fast, and forgets everything on restart."""

    def __init__(self):
        self._events = {}
        self._next_id = 1

    def add(self, event):
        event.id = self._next_id
        self._events[event.id] = event
        self._next_id += 1
        return event

    def get(self, event_id):
        return self._events.get(event_id)

    def all(self):
        return list(self._events.values())

    def update(self, event_id, event):
        if event_id not in self._events:
            return None
        event.id = event_id
        self._events[event_id] = event
        return event
