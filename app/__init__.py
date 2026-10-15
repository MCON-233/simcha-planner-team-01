from collections.abc import Mapping
from typing import Any

from flask import Flask

from .repositories.event_repository import InMemoryEventRepository
from .services.event_service import EventService


def create_app(test_config: Mapping[str, Any] | None = None) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)

    if test_config is not None:
        app.config.from_mapping(test_config)

    # The one place that chooses the repository implementation.
    app.extensions["event_service"] = EventService(InMemoryEventRepository())

    from .event_routes import bp as events_bp
    from .routes import bp

    app.register_blueprint(bp)
    app.register_blueprint(events_bp)
    return app
