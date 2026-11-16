"""OpenAIProvider tests that never reach the internet: the OpenAI client is replaced by a stand-in."""
from types import SimpleNamespace

import openai
import pytest

from app.ai.ai_provider import AIProviderError
from app.ai.openai_provider import OpenAIProvider


class StandInResponses:
    def __init__(self, reply=None, error=None):
        self.reply = reply
        self.error = error
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        if self.error is not None:
            raise self.error
        return SimpleNamespace(output_text=self.reply)


def provider_with(responses):
    return OpenAIProvider(api_key="test-key", model="test-model",
                          client=SimpleNamespace(responses=responses))


def test_returns_the_model_text():
    assert provider_with(StandInResponses(reply="1. Book a hall")).complete("Be brief.", "Ideas please") == "1. Book a hall"


def test_sends_the_model_instructions_and_prompt():
    responses = StandInResponses(reply="ok")

    provider_with(responses).complete("Be brief.", "Ideas please")

    assert responses.calls == [{"model": "test-model", "instructions": "Be brief.", "input": "Ideas please"}]


def test_openai_errors_become_ai_provider_errors():
    responses = StandInResponses(error=openai.APIConnectionError(request=None))

    with pytest.raises(AIProviderError):
        provider_with(responses).complete("Be brief.", "Ideas please")


def test_no_api_key_is_an_ai_provider_error():
    with pytest.raises(AIProviderError):
        OpenAIProvider(api_key=None).complete("Be brief.", "Ideas please")
