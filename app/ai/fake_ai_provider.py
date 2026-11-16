from app.ai.ai_provider import AIProvider, AIProviderError

CANNED_REPLY = """1. Choose a theme that matches the season
2. Book the hall early
3. Plan a simple, elegant menu"""


class FakeAIProvider(AIProvider):
    """Used in tests: answers instantly, costs nothing, and remembers what it was asked."""

    def __init__(self, reply: str = CANNED_REPLY, error: AIProviderError | None = None):
        self.reply = reply
        self.error = error
        self.prompts: list[str] = []

    def complete(self, instructions: str, prompt: str) -> str:
        self.prompts.append(prompt)
        if self.error is not None:
            raise self.error
        return self.reply
