from datetime import date


class Event:
    def __init__(self, event_type: str, event_date: date, guest_count: int, budget: float) -> None:
        if guest_count < 1:
            raise ValueError("Guest count must be at least 1.")
        self.event_type = event_type
        self.event_date = event_date
        self.guest_count = guest_count
        self.budget = budget
