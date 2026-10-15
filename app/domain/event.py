from datetime import date


class Event:
    def __init__(self, event_type, event_date, guest_count, budget):
        if guest_count < 1:
            raise ValueError("Guest count must be at least 1")
        if budget < 0:
            raise ValueError("Budget must be non-negative")
        if not isinstance(event_date, (str, date)):
            raise ValueError("Event date must be a string or a date object")
        if event_date < date.today():
            raise ValueError("Event date must be in the future")
        self.event_type = event_type
        self.event_date = event_date
        self.guest_count = guest_count
        self.budget = budget

    def days_until_event(self, the_date=date.today()):
        if isinstance(self.event_date, str):
            raise ValueError("Event date is a string; cannot compute days until event")
        return (self.event_date - the_date).days