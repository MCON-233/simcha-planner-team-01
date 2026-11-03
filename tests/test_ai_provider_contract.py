"""Contract tests: every AIProvider must pass all of these.

Each test runs once per implementation listed in PROVIDERS.
No test reaches the internet: OpenAIProvider gets a stand-in client.
"""
from types import SimpleNamespace

import openai
import pytest

from app.ai.ai_provider import AIProvider, AIProviderError
from app.ai.fake_ai_provider import FakeAIProvider
from app.ai.openai_provider import OpenAIProvider

PROVIDERS = ["fake", "openai"]

REPLY = "1. Book a hall\n2. Plan the menu"


class StandInResponses:
    def __init__(self, reply=None, error=None):
        self.reply = reply
        self.error = error

    def create(self, **kwargs):
        if self.error is not None:
            raise self.error
        return SimpleNamespace(output_text=self.reply)


def build(kind, reply=REPLY, failing=False):
    if kind == "fake":
        return FakeAIProvider(reply=reply, error=AIProviderError("down") if failing else None)
    error = openai.APIConnectionError(request=None) if failing else None
    client = SimpleNamespace(responses=StandInResponses(reply=reply, error=error))
    return OpenAIProvider(api_key="test-key", model="test-model", client=client)


@pytest.fixture(params=PROVIDERS)
def kind(request):
    return request.param


# ---- Shape ----

def test_is_an_ai_provider(kind):
    assert isinstance(build(kind), AIProvider)


# ---- Answering ----

def test_complete_returns_the_reply_text(kind):
    assert build(kind, reply=REPLY).complete("Be brief.", "Ideas please") == REPLY


def test_complete_returns_a_string(kind):
    assert isinstance(build(kind).complete("Be brief.", "Ideas please"), str)


def test_complete_can_be_called_more_than_once(kind):
    provider = build(kind)

    provider.complete("Be brief.", "Ideas please")

    assert provider.complete("Be brief.", "More ideas") == REPLY


# ---- Failing ----

def test_failure_raises_ai_provider_error(kind):
    with pytest.raises(AIProviderError):
        build(kind, failing=True).complete("Be brief.", "Ideas please")
