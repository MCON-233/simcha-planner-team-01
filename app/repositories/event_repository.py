from app.domain.event import Event


class InMemoryEventRepository:
    """Keeps events in a dictionary.

    Used by unit tests, and for now by the running app as well. Events are lost
    when the app restarts; replacing this with a database-backed repository is
    recorded in the technical-debt log.
    """

    def __init__(self) -> None:
        self._events: dict[int, Event] = {}
        self._next_id = 1

    def add(self, event: Event) -> Event:
        event.id = self._next_id
        self._events[event.id] = event
        self._next_id += 1
        return event

    def get(self, event_id: int) -> Event | None:
        return self._events.get(event_id)

    def all(self) -> list[Event]:
        return list(self._events.values())
