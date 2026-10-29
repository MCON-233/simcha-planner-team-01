from datetime import date, timedelta

import pytest

from app import create_app
from app.ai.ai_provider import AIProviderError
from app.ai.fake_ai_provider import FakeAIProvider


def future(days=30):
    return date.today() + timedelta(days=days)


@pytest.fixture
def wedding_like(service):
    return service.create_event("sheva_brachos", future(), guest_count=200, budget=25000)


def test_suggest_ideas_shows_the_ideas(client, wedding_like):
    response = client.post(f"/events/{wedding_like.id}/ideas")

    assert response.status_code == 200
    assert "Book the hall early" in response.get_data(as_text=True)


def test_the_ideas_use_the_event_details(client, ai, wedding_like):
    client.post(f"/events/{wedding_like.id}/ideas")

    assert "Sheva brachos" in ai.prompts[0]
    assert "200" in ai.prompts[0]
    assert "$25,000" in ai.prompts[0]


def test_ideas_for_an_unknown_event_are_not_found(client, ai):
    assert client.post("/events/999/ideas").status_code == 404
    assert ai.prompts == []


def test_ai_failure_shows_a_friendly_message(client, ai, wedding_like):
    ai.error = AIProviderError("credit_balance_exhausted")

    response = client.post(f"/events/{wedding_like.id}/ideas")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Ideas are not available right now" in html
    assert "credit_balance_exhausted" not in html   # never show the raw error to the host


def test_suggest_ideas_without_a_csrf_token_is_rejected():
    ai = FakeAIProvider()
    app = create_app({"TESTING": True}, ai_provider=ai)
    event = app.extensions["event_service"].create_event("vort", future(), guest_count=50, budget=1000)

    response = app.test_client().post(f"/events/{event.id}/ideas")

    assert response.status_code == 400
    assert ai.prompts == []


def test_testing_app_uses_the_fake_ai_by_default():
    app = create_app({"TESTING": True})

    assert isinstance(app.extensions["ai_provider"], FakeAIProvider)
