import os
from collections.abc import Mapping
from typing import Any

from flask import Flask

from .repositories.event_repository import EventRepository
from .repositories.in_memory_event_repository import InMemoryEventRepository
from .services.event_service import EventService


def create_app(test_config: Mapping[str, Any] | None = None,
               repository: EventRepository | None = None) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    # Signs the CSRF tokens Flask-WTF puts in every form. Set SECRET_KEY in production.
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev")

    if test_config is not None:
        app.config.from_mapping(test_config)

    # The one place that chooses the repository implementation.
    if repository is None:
        repository = InMemoryEventRepository()
    app.extensions["event_service"] = EventService(repository)

    from .event_routes import bp as events_bp
    from .routes import bp

    app.register_blueprint(bp)
    app.register_blueprint(events_bp)
    return app
