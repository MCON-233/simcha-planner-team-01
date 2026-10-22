from datetime import date, timedelta

import pytest

from app.domain.event import EVENT_TYPES, Event


def future(days=30):
    return date.today() + timedelta(days=days)


def test_event_keeps_its_details():
    event = Event("bar_mitzvah", future(), guest_count=120, budget=15000)

    assert event.event_type == "bar_mitzvah"
    assert event.event_date == future()
    assert event.guest_count == 120
    assert event.budget == 15000


def test_new_event_has_no_id_yet():
    event = Event("bar_mitzvah", future(), guest_count=120, budget=15000)

    assert event.id is None


def test_event_type_must_be_in_the_allowed_set():
    with pytest.raises(ValueError, match="Event type must be one of"):
        Event("pool_party", future(), guest_count=120, budget=15000)


def test_every_allowed_event_type_is_accepted():
    for event_type in EVENT_TYPES:
        assert Event(event_type, future(), guest_count=10, budget=0).event_type == event_type


def test_guest_count_must_be_at_least_one():
    with pytest.raises(ValueError, match="Guest count must be at least 1"):
        Event("bar_mitzvah", future(), guest_count=0, budget=15000)


def test_budget_must_be_non_negative():
    with pytest.raises(ValueError, match="Budget must be non-negative"):
        Event("bar_mitzvah", future(), guest_count=120, budget=-100)


def test_event_date_must_be_a_date():
    with pytest.raises(ValueError, match="Event date must be a date"):
        Event("bar_mitzvah", "10/20/2026", guest_count=120, budget=15000)


def test_event_date_must_be_in_future():
    with pytest.raises(ValueError, match="Event date must be in the future"):
        Event("bar_mitzvah", date.today() - timedelta(days=1), guest_count=120, budget=15000)


def test_event_date_cannot_be_today():
    with pytest.raises(ValueError, match="Event date must be in the future"):
        Event("bar_mitzvah", date.today(), guest_count=120, budget=15000)


def test_days_until_event_calculation():
    event = Event("bar_mitzvah", future(10), guest_count=120, budget=15000)

    assert event.days_until_event() == 10
    assert event.days_until_event(date.today() + timedelta(days=5)) == 5


def test_one_guest_is_accepted():
    assert Event("bar_mitzvah", future(), guest_count=1, budget=15000).guest_count == 1


def test_zero_budget_is_accepted():
    assert Event("bar_mitzvah", future(), guest_count=120, budget=0).budget == 0


def test_budget_just_below_zero_is_rejected():
    with pytest.raises(ValueError, match="Budget must be non-negative"):
        Event("bar_mitzvah", future(), guest_count=120, budget=-0.01)


def test_tomorrow_is_accepted():
    assert Event("bar_mitzvah", future(1), guest_count=120, budget=15000).event_date == future(1)


def test_days_until_event_is_zero_on_the_day():
    event = Event("bar_mitzvah", future(10), guest_count=120, budget=15000)

    assert event.days_until_event(future(10)) == 0


def test_days_until_event_matches_date_subtraction():
    event = Event("bar_mitzvah", future(45), guest_count=120, budget=15000)

    assert event.days_until_event() == (event.event_date - date.today()).days
