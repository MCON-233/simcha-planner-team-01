from datetime import date, timedelta

import pytest

from app import create_app


def future(days=30):
    return date.today() + timedelta(days=days)


@pytest.fixture
def event(service):
    return service.create_event("vort", future(), guest_count=50, budget=1000)


@pytest.fixture
def checklist(app):
    return app.extensions["checklist_service"]


def test_event_page_says_when_the_checklist_is_empty(client, event):
    html = client.get(f"/events/{event.id}").get_data(as_text=True)

    assert "Checklist" in html
    assert "No checklist items yet" in html


def test_event_page_shows_the_events_checklist_items(client, event, checklist):
    checklist.add_item(event.id, "Book venue")

    html = client.get(f"/events/{event.id}").get_data(as_text=True)

    assert "Book venue" in html
    assert "No checklist items yet" not in html


def test_adding_an_item_shows_it_on_the_event_page(client, event):
    response = client.post(f"/events/{event.id}/checklist", data={"title": "Book venue"})

    assert response.status_code == 302
    assert response.headers["Location"].endswith(f"/events/{event.id}")
    assert "Book venue" in client.get(f"/events/{event.id}").get_data(as_text=True)


def test_blank_item_shows_an_error(client, event, checklist):
    response = client.post(f"/events/{event.id}/checklist", data={"title": "   "})

    assert response.status_code == 400
    assert "Checklist item needs a title" in response.get_data(as_text=True)
    assert checklist.items_for_event(event.id) == []


def test_missing_title_shows_an_error(client, event):
    response = client.post(f"/events/{event.id}/checklist", data={})

    assert response.status_code == 400
    assert "Checklist item needs a title" in response.get_data(as_text=True)


def test_adding_an_item_to_an_unknown_event_is_not_found(client):
    response = client.post("/events/999/checklist", data={"title": "Book venue"})

    assert response.status_code == 404


def test_ticking_an_item_marks_it_done(client, event, checklist):
    item = checklist.add_item(event.id, "Book venue")

    response = client.post(f"/events/{event.id}/checklist/{item.id}/toggle")

    assert response.status_code == 302
    assert checklist.items_for_event(event.id)[0].done is True
    html = client.get(f"/events/{event.id}").get_data(as_text=True)
    assert 'class="checklist-item done"' in html
    assert "Mark not done" in html


def test_ticking_an_unknown_item_is_not_found(client, event):
    assert client.post(f"/events/{event.id}/checklist/999/toggle").status_code == 404


def test_checklist_forms_are_protected_against_cross_site_requests():
    app = create_app({"TESTING": True})
    event = app.extensions["event_service"].create_event("vort", future(), guest_count=50, budget=1000)
    app.extensions["checklist_service"].add_item(event.id, "Book venue")
    client = app.test_client()

    html = client.get(f"/events/{event.id}").get_data(as_text=True)

    assert html.count('name="csrf_token"') >= 3   # ideas, add item, tick item
    assert client.post(f"/events/{event.id}/checklist", data={"title": "Sneaky"}).status_code == 400
