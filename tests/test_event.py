from datetime import date, timedelta

import pytest

from app.domain.event import Event


def future(days=30):
    return date.today() + timedelta(days=days)


# Acceptance criterion 1
def test_event_keeps_its_details():
    event = Event("bar_mitzvah", future(), guest_count=120, budget=15000)

    assert event.event_type == "bar_mitzvah"
    assert event.guest_count == 120
    assert event.budget == 15000

def test_guest_count_must_be_at_least_one():
    with pytest.raises(ValueError):
        Event("bar_mitzvah", future(), guest_count=0, budget=15000)

def test_budget_must_be_non_negative():
    with pytest.raises(ValueError):
        Event("bar_mitzvah", future(), guest_count=120, budget=-100)

def test_event_date_must_be_in_future():
    with pytest.raises(ValueError):
        Event("bar_mitzvah", date.today() - timedelta(days=1), guest_count=120, budget=15000)

def test_days_until_event_calculation():
    event = Event("bar_mitzvah", future(10), guest_count=120, budget=15000)
    assert event.days_until_event() == 10
    assert event.days_until_event(date.today() + timedelta(days=5)) == 5