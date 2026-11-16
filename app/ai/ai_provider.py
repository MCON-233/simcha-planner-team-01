from abc import ABC, abstractmethod


class AIProviderError(Exception):
    """The AI could not answer: no key, no credit, network down, timeout..."""


class AIProvider(ABC):
    """Anything that can send a prompt to a language model and return its text."""

    @abstractmethod
    def complete(self, instructions: str, prompt: str) -> str:
        """Return the model's reply. Raise AIProviderError if there is no reply."""
