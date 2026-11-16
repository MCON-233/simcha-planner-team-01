from datetime import date, timedelta

import pytest

from app.ai.ai_provider import AIProviderError
from app.ai.fake_ai_provider import FakeAIProvider
from app.domain.event import Event
from app.repositories.in_memory_event_repository import InMemoryEventRepository
from app.services.idea_service import IdeaService, build_prompt, parse_ideas


def future(days=30):
    return date.today() + timedelta(days=days)


@pytest.fixture
def repo():
    return InMemoryEventRepository()


@pytest.fixture
def ai():
    return FakeAIProvider()


@pytest.fixture
def ideas(repo, ai):
    return IdeaService(repo, ai)


@pytest.fixture
def bar_mitzvah(repo):
    return repo.add(Event("bar_mitzvah", future(), guest_count=150, budget=12000))


def test_prompt_uses_the_event_details():
    prompt = build_prompt(Event("bar_mitzvah", future(), guest_count=150, budget=12000))

    assert "Bar mitzvah" in prompt
    assert "150" in prompt
    assert "$12,000" in prompt


def test_reply_becomes_a_clean_list():
    assert parse_ideas("1. Book a hall\n\n2) Hire a band\n- Send invitations") == [
        "Book a hall", "Hire a band", "Send invitations",
    ]


def test_suggest_ideas_returns_the_parsed_ideas(ideas, bar_mitzvah):
    assert ideas.suggest_ideas(bar_mitzvah.id) == [
        "Choose a theme that matches the season",
        "Book the hall early",
        "Plan a simple, elegant menu",
    ]


def test_suggest_ideas_sends_the_event_to_the_ai(ideas, ai, bar_mitzvah):
    ideas.suggest_ideas(bar_mitzvah.id)

    assert len(ai.prompts) == 1
    assert "Bar mitzvah" in ai.prompts[0]


def test_unknown_event_returns_none_and_does_not_call_the_ai(ideas, ai):
    assert ideas.suggest_ideas(999) is None
    assert ai.prompts == []


def test_ai_failure_is_passed_on(ideas, ai, bar_mitzvah):
    ai.error = AIProviderError("no credit")

    with pytest.raises(AIProviderError):
        ideas.suggest_ideas(bar_mitzvah.id)
