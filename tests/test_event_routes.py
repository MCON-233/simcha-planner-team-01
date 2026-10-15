from datetime import date, timedelta


def future(days=10):
    return date.today() + timedelta(days=days)


# See my events

def test_events_page_says_when_there_are_no_events(client):
    response = client.get("/events")

    assert response.status_code == 200
    assert "no events yet" in response.get_data(as_text=True)


def test_events_page_lists_saved_events_with_links(client, service):
    event = service.create_event("vort", future(), guest_count=50, budget=1000)

    html = client.get("/events").get_data(as_text=True)

    assert "Vort" in html
    assert f'href="/events/{event.id}"' in html


def test_event_page_shows_the_days_remaining(client, service):
    event = service.create_event("vort", future(10), guest_count=50, budget=1000)

    response = client.get(f"/events/{event.id}")

    assert response.status_code == 200
    assert "10 days to go" in response.get_data(as_text=True)


def test_unknown_event_shows_not_found(client):
    response = client.get("/events/999")

    assert response.status_code == 404
    assert "Event not found" in response.get_data(as_text=True)


# Create an event

def valid_form(**changes):
    form = {
        "event_type": "vort",
        "event_date": future(10).isoformat(),
        "guest_count": "50",
        "budget": "1000",
    }
    form.update(changes)
    return form


def test_new_event_form_is_shown(client):
    response = client.get("/events/new")

    assert response.status_code == 200
    assert 'name="event_date"' in response.get_data(as_text=True)


def test_creating_an_event_redirects_to_its_page(client):
    response = client.post("/events", data=valid_form())

    assert response.status_code == 302
    assert response.headers["Location"].startswith("/events/")


def test_created_event_appears_in_my_events(client, service):
    client.post("/events", data=valid_form())

    assert len(service.list_events()) == 1
