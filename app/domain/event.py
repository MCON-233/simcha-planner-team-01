from datetime import date

EVENT_TYPES = {"bar_mitzvah", "bat_mitzvah", "vort", "sheva_brachos"}


class Event:
    def __init__(self, event_type, event_date, guest_count, budget):
        self._validate(event_type, event_date, guest_count, budget)
        self.id = None
        self.event_type = event_type
        self.event_date = event_date
        self.guest_count = guest_count
        self.budget = budget

    def days_until_event(self, the_date=None):
        if the_date is None:
            the_date = date.today()
        return (self.event_date - the_date).days

    @staticmethod
    def _validate(event_type, event_date, guest_count, budget):
        if event_type not in EVENT_TYPES:
            raise ValueError(f"Event type must be one of: {', '.join(sorted(EVENT_TYPES))}")
        if not isinstance(event_date, date):
            raise ValueError("Event date must be a date")
        if event_date <= date.today():
            raise ValueError("Event date must be in the future")
        if guest_count < 1:
            raise ValueError("Guest count must be at least 1")
        if budget < 0:
            raise ValueError("Budget must be non-negative")
