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


# Fix my mistakes

def test_zero_guests_shows_the_form_again_with_a_message(client):
    response = client.post("/events", data=valid_form(guest_count="0"))

    assert response.status_code == 400
    assert "Guest count must be at least 1" in response.get_data(as_text=True)


def test_invalid_input_keeps_what_the_host_typed(client):
    response = client.post("/events", data=valid_form(guest_count="0", budget="2500"))

    assert 'value="2500"' in response.get_data(as_text=True)


def test_text_instead_of_a_number_shows_a_message(client):
    response = client.post("/events", data=valid_form(guest_count="abc"))

    assert response.status_code == 400
    assert "Please enter a valid date, guest count, and budget." in response.get_data(as_text=True)


def test_invalid_input_saves_nothing(client, service):
    client.post("/events", data=valid_form(guest_count="0"))

    assert service.list_events() == []


# Update an event

def test_event_page_links_to_its_edit_form(client, service):
    event = service.create_event("vort", future(), guest_count=50, budget=1000)

    html = client.get(f"/events/{event.id}").get_data(as_text=True)

    assert f'href="/events/{event.id}/edit"' in html


def test_edit_form_shows_the_current_values(client, service):
    event = service.create_event("vort", future(), guest_count=50, budget=1000)

    response = client.get(f"/events/{event.id}/edit")

    assert response.status_code == 200
    assert 'value="50"' in response.get_data(as_text=True)


def test_editing_an_unknown_event_shows_not_found(client):
    assert client.get("/events/999/edit").status_code == 404
    assert client.post("/events/999/edit", data=valid_form()).status_code == 404


def test_updating_an_event_saves_it_and_redirects_to_its_page(client, service):
    event = service.create_event("vort", future(), guest_count=50, budget=1000)

    response = client.post(f"/events/{event.id}/edit", data=valid_form(guest_count="120"))

    assert response.status_code == 302
    assert response.headers["Location"] == f"/events/{event.id}"
    assert service.get_event(event.id).guest_count == 120


def test_invalid_update_shows_the_form_again_and_changes_nothing(client, service):
    event = service.create_event("vort", future(), guest_count=50, budget=1000)

    response = client.post(f"/events/{event.id}/edit", data=valid_form(guest_count="0", budget="2500"))

    html = response.get_data(as_text=True)
    assert response.status_code == 400
    assert "Guest count must be at least 1" in html
    assert 'value="2500"' in html
    assert service.get_event(event.id).guest_count == 50


# Boundaries, round trips, and more mistakes

def test_created_event_page_shows_what_the_host_typed(client):
    form = valid_form(event_type="bar_mitzvah", guest_count="120", budget="2500")

    response = client.post("/events", data=form, follow_redirects=True)

    html = response.get_data(as_text=True)
    event_date = future(10)
    assert "Bar mitzvah" in html
    assert f"{event_date.strftime('%B')} {event_date.day}, {event_date.year}" in html
    assert "120" in html
    assert "$2,500.00" in html


def test_created_event_is_saved_with_the_typed_values(client, service):
    client.post("/events", data=valid_form(event_type="bar_mitzvah", guest_count="120", budget="2500"))

    [event] = service.list_events()
    assert event.event_type == "bar_mitzvah"
    assert event.event_date == future(10)
    assert event.guest_count == 120
    assert event.budget == 2500


def test_created_event_appears_on_the_events_page_and_in_the_service(client, service):
    client.post("/events", data=valid_form())

    html = client.get("/events").get_data(as_text=True)
    [event] = service.list_events()
    assert f'href="/events/{event.id}"' in html


def test_one_guest_is_accepted_by_the_form(client):
    assert client.post("/events", data=valid_form(guest_count="1")).status_code == 302


def test_missing_field_shows_a_message(client, service):
    form = valid_form()
    del form["event_date"]

    response = client.post("/events", data=form)

    assert response.status_code == 400
    assert "Please enter a valid date, guest count, and budget." in response.get_data(as_text=True)
    assert service.list_events() == []


def test_past_date_shows_a_message(client):
    response = client.post("/events", data=valid_form(event_date=future(-1).isoformat()))

    assert response.status_code == 400
    assert "Event date must be in the future" in response.get_data(as_text=True)


def test_unknown_event_type_shows_a_message(client):
    response = client.post("/events", data=valid_form(event_type="pool_party"))

    assert response.status_code == 400
    assert "Event type must be one of" in response.get_data(as_text=True)


def test_updating_an_event_saves_every_field(client, service):
    event = service.create_event("vort", future(), guest_count=50, budget=1000)

    client.post(f"/events/{event.id}/edit",
                data=valid_form(event_type="bat_mitzvah", event_date=future(20).isoformat(),
                                guest_count="80", budget="3000"))

    updated = service.get_event(event.id)
    assert updated.event_type == "bat_mitzvah"
    assert updated.event_date == future(20)
    assert updated.guest_count == 80
    assert updated.budget == 3000


def test_updated_event_page_shows_the_new_values(client, service):
    event = service.create_event("vort", future(), guest_count=50, budget=1000)

    response = client.post(f"/events/{event.id}/edit", data=valid_form(guest_count="80", budget="3000"),
                           follow_redirects=True)

    html = response.get_data(as_text=True)
    assert "80" in html
    assert "$3,000.00" in html


def test_text_instead_of_a_number_on_edit_shows_a_message(client, service):
    event = service.create_event("vort", future(), guest_count=50, budget=1000)

    response = client.post(f"/events/{event.id}/edit", data=valid_form(budget="lots"))

    assert response.status_code == 400
    assert "Please enter a valid date, guest count, and budget." in response.get_data(as_text=True)
    assert service.get_event(event.id).budget == 1000


def test_missing_field_on_edit_changes_nothing(client, service):
    event = service.create_event("vort", future(), guest_count=50, budget=1000)
    form = valid_form(guest_count="80")
    del form["budget"]

    response = client.post(f"/events/{event.id}/edit", data=form)

    assert response.status_code == 400
    assert service.get_event(event.id).guest_count == 50
