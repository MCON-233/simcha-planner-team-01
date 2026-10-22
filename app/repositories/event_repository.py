from abc import ABC, abstractmethod


class EventRepository(ABC):
    """What every event repository can do. Says nothing about how."""

    @abstractmethod
    def add(self, event):
        """Save a new event, give it an id, and return it."""

    @abstractmethod
    def get(self, event_id):
        """Return the event with this id, or None."""

    @abstractmethod
    def all(self):
        """Return every saved event."""

    @abstractmethod
    def update(self, event):
        """Replace the saved event that has this event's id, and return it."""


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

    def update(self, event):
        self._events[event.id] = event
        return event
