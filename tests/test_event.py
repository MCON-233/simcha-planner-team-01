from datetime import date, timedelta

import pytest

from app.domain.event import Event


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
