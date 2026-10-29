import os
from collections.abc import Mapping
from typing import Any

from dotenv import load_dotenv
from flask import Flask

from app.db import db

from .ai.ai_provider import AIProvider
from .ai.fake_ai_provider import FakeAIProvider
from .ai.openai_provider import OpenAIProvider

from .repositories.event_repository import EventRepository
from .repositories.in_memory_event_repository import InMemoryEventRepository
from .repositories.sqlalchemy_event_repository import SqlAlchemyEventRepository
from .services.event_service import EventService
from .services.idea_service import IdeaService


def create_app(test_config: Mapping[str, Any] | None = None,
               repository: EventRepository | None = None,
               ai_provider: AIProvider | None = None) -> Flask:
    """Create and configure the Flask application."""
    load_dotenv()   # copies OPENAI_API_KEY and the other settings from .env into os.environ
    app = Flask(__name__)
    # Signs the CSRF tokens Flask-WTF puts in every form. Set SECRET_KEY in production.
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev")

    if test_config is not None:
        app.config.from_mapping(test_config)

    app.config.setdefault(
        "SQLALCHEMY_DATABASE_URI",
        os.getenv("DATABASE_URL", "sqlite:///simcha.db"),
    )
    db.init_app(app)
    with app.app_context():
        from app.models import event_model  # noqa: F401  registers the events table
        db.create_all()

    # The one place that chooses the repository implementation.
    if repository is None:
        if app.config.get("TESTING"):
            repository = InMemoryEventRepository()   # a test can never touch the real database by accident
        else:
            repository = SqlAlchemyEventRepository()
    app.extensions["event_service"] = EventService(repository)

    # The one place that chooses which AI the app talks to.
    if ai_provider is None:
        if app.config.get("TESTING"):
            ai_provider = FakeAIProvider()   # tests never make a paid call
        else:
            ai_provider = OpenAIProvider(
                api_key=os.getenv("OPENAI_API_KEY"),
                model=os.getenv("OPENAI_MODEL", "gpt-5.6-luna"),
            )
    app.extensions["ai_provider"] = ai_provider
    app.extensions["idea_service"] = IdeaService(repository, ai_provider)

    from .event_routes import bp as events_bp
    from .routes import bp

    app.register_blueprint(bp)
    app.register_blueprint(events_bp)
    return app
