from datetime import date

EVENT_TYPES: frozenset[str] = frozenset(
    {"bar_mitzvah", "bat_mitzvah", "vort", "sheva_brachos", "community_dinner", "birthday"}
)


class Event:
    def __init__(
        self,
        event_type: str,
        event_date: date,
        guest_count: int,
        budget: float,
        venue: str = "",
        theme: str = "",
    ) -> None:
        self._validate(event_type, event_date, guest_count, budget)
        self.id: int | None = None
        self.event_type = event_type
        self.event_date = event_date
        self.guest_count = guest_count
        self.budget = budget
        self.venue = venue
        self.theme = theme

    def days_until(self, today: date) -> int:
        return (self.event_date - today).days

    @staticmethod
    def _validate(event_type: str, event_date: date, guest_count: int, budget: float) -> None:
        if event_type not in EVENT_TYPES:
            raise ValueError(f"Unsupported event type: {event_type}.")
        if guest_count < 1:
            raise ValueError("Guest count must be at least 1.")
        if event_date <= date.today():
            raise ValueError("The event date must be in the future.")
        if budget < 0:
            raise ValueError("The budget cannot be negative.")
