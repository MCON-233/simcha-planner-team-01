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
    def update(self, event_id, event):
        """Replace the saved event with this id by event, and return it (None if there is none)."""
