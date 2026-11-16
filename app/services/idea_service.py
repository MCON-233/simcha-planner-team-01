from app.ai.ai_provider import AIProvider
from app.domain.event import Event
from app.repositories.event_repository import EventRepository

INSTRUCTIONS = (
    "You are a helpful planner for Jewish simchas. "
    "Reply with exactly 5 short, practical ideas, one per line, numbered 1 to 5. "
    "No introduction and no closing sentence."
)


def build_prompt(event: Event) -> str:
    """Turn the event's details into the question we send to the model."""
    event_type = event.event_type.replace("_", " ").capitalize()
    return (
        "Suggest ideas for planning this event.\n"
        f"Event type: {event_type}\n"
        f"Date: {event.event_date.isoformat()}\n"
        f"Guests: {event.guest_count}\n"
        f"Budget: ${event.budget:,.0f}"
    )


def parse_ideas(text: str) -> list[str]:
    """One idea per non-empty line, with numbers and bullets removed; at most five."""
    ideas = []
    for line in text.splitlines():
        idea = line.strip().lstrip("-*•0123456789.) ").strip()
        if idea:
            ideas.append(idea)
    return ideas[:5]


class IdeaService:
    def __init__(self, repository: EventRepository, ai_provider: AIProvider):
        self._repository = repository
        self._ai = ai_provider

    def suggest_ideas(self, event_id):
        """Ideas for this event, or None if there is no such event. Raises AIProviderError if the AI fails."""
        event = self._repository.get(event_id)
        if event is None:
            return None
        return parse_ideas(self._ai.complete(INSTRUCTIONS, build_prompt(event)))
