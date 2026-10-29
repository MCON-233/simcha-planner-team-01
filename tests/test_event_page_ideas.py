from datetime import date, timedelta

from app import create_app


def future(days=30):
    return date.today() + timedelta(days=days)


def test_event_page_has_a_suggest_ideas_button(client, service):
    event = service.create_event("vort", future(), guest_count=50, budget=1000)

    html = client.get(f"/events/{event.id}").get_data(as_text=True)

    assert f'action="/events/{event.id}/ideas"' in html
    assert "Suggest ideas" in html


def test_suggest_ideas_button_is_protected_against_cross_site_requests():
    app = create_app({"TESTING": True})
    event = app.extensions["event_service"].create_event("vort", future(), guest_count=50, budget=1000)

    html = app.test_client().get(f"/events/{event.id}").get_data(as_text=True)

    assert 'name="csrf_token"' in html
