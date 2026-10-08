from datetime import date, timedelta

import pytest

from app.domain.event import EVENT_TYPES, Event


def future(days: int = 30) -> date:
    return date.today() + timedelta(days=days)


def test_event_keeps_its_details() -> None:
    event = Event("bar_mitzvah", future(), guest_count=120, budget=15000)

    assert event.event_type == "bar_mitzvah"
    assert event.guest_count == 120
    assert event.budget == 15000


def test_guest_count_must_be_at_least_one() -> None:
    with pytest.raises(ValueError):
        Event("bar_mitzvah", future(), guest_count=0, budget=15000)


def test_event_date_must_be_in_the_future() -> None:
    yesterday = date.today() - timedelta(days=1)

    with pytest.raises(ValueError):
        Event("vort", yesterday, guest_count=80, budget=5000)


def test_budget_cannot_be_negative() -> None:
    with pytest.raises(ValueError):
        Event("vort", future(), guest_count=80, budget=-1)


def test_event_type_must_be_supported() -> None:
    with pytest.raises(ValueError):
        Event("pool_party", future(), guest_count=80, budget=5000)


def test_every_supported_event_type_is_accepted() -> None:
    for event_type in EVENT_TYPES:
        event = Event(event_type, future(), guest_count=10, budget=0)
        assert event.event_type == event_type


def test_venue_and_theme_are_optional() -> None:
    event = Event("sheva_brachos", future(), guest_count=40, budget=2000)

    assert event.venue == ""
    assert event.theme == ""


def test_venue_and_theme_are_kept_when_given() -> None:
    event = Event(
        "bat_mitzvah", future(), guest_count=75, budget=4000, venue="School social hall", theme="Garden"
    )

    assert event.venue == "School social hall"
    assert event.theme == "Garden"


def test_days_until_counts_from_the_given_day() -> None:
    event = Event("birthday", future(10), guest_count=20, budget=500)

    assert event.days_until(date.today()) == 10
    assert event.days_until(date.today() + timedelta(days=3)) == 7
