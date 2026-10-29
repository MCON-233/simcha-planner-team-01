import openai

from app.ai.ai_provider import AIProvider, AIProviderError


class OpenAIProvider(AIProvider):
    """Makes the OpenAI SDK look like our AIProvider. The only file that imports openai."""

    def __init__(self, api_key: str | None, model: str = "gpt-5.6-luna", client=None):
        self._model = model
        if client is not None:
            self._client = client
        elif api_key:
            self._client = openai.OpenAI(api_key=api_key, timeout=30)
        else:
            self._client = None

    def complete(self, instructions: str, prompt: str) -> str:
        if self._client is None:
            raise AIProviderError("OPENAI_API_KEY is not set")
        try:
            response = self._client.responses.create(
                model=self._model,
                instructions=instructions,
                input=prompt,
            )
        except openai.OpenAIError as error:
            raise AIProviderError(str(error)) from error
        return response.output_text
