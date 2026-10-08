from datetime import date, timedelta

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app


@pytest.fixture()
def app() -> Flask:
    return create_app({"TESTING": True})


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()


def valid_form(**overrides: str) -> dict[str, str]:
    form = {
        "event_type": "bat_mitzvah",
        "event_date": (date.today() + timedelta(days=30)).isoformat(),
        "guest_count": "75",
        "budget": "4000",
        "venue": "School social hall",
        "theme": "Garden",
    }
    form.update(overrides)
    return form


def test_new_event_form_is_shown(client: FlaskClient) -> None:
    response = client.get("/events/new")

    assert response.status_code == 200
    assert '<form method="post"' in response.get_data(as_text=True)


def test_valid_event_redirects_to_its_dashboard(client: FlaskClient) -> None:
    response = client.post("/events", data=valid_form())

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/events/1")


def test_dashboard_shows_saved_details_and_countdown(client: FlaskClient) -> None:
    client.post("/events", data=valid_form())

    html = client.get("/events/1").get_data(as_text=True)

    assert "School social hall" in html
    assert "Garden" in html
    assert "75" in html
    assert "30 days" in html


def test_invalid_event_shows_message_and_is_not_saved(app: Flask, client: FlaskClient) -> None:
    response = client.post("/events", data=valid_form(guest_count="0"))

    assert response.status_code == 400
    assert "Guest count must be at least 1." in response.get_data(as_text=True)
    assert app.extensions["event_service"].get_event(1) is None


def test_unreadable_number_shows_message(client: FlaskClient) -> None:
    response = client.post("/events", data=valid_form(budget="lots"))

    assert response.status_code == 400
    assert "Please enter a valid date" in response.get_data(as_text=True)


def test_unknown_event_shows_not_found_page(client: FlaskClient) -> None:
    response = client.get("/events/999")

    assert response.status_code == 404
    assert "We could not find that event" in response.get_data(as_text=True)
