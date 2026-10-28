from abc import ABC, abstractmethod

from sqlalchemy import select

from app.domain.event import Event


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
        """Replace the saved event that has this event's id, and return it (None if there is none)."""


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


class SqlAlchemyEventRepository(EventRepository):
    """Keeps events in a database using SQLAlchemy. Survives restarts."""

    def __init__(self, db_session):
        self._db_session = db_session

    def add(self, event):
        self._db_session.add(event)
        self._db_session.commit()   # the database gives the event its id
        return event

    def get(self, event_id):
        return self._db_session.get(Event, event_id)

    def all(self):
        return list(self._db_session.scalars(select(Event)))

    def update(self, event):
        existing_event = self.get(event.id)
        if existing_event is None:
            return None
        existing_event.event_type = event.event_type
        existing_event.event_date = event.event_date
        existing_event.guest_count = event.guest_count
        existing_event.budget = event.budget
        self._db_session.commit()
        return existing_event
