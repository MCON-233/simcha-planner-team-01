import os
from collections.abc import Mapping
from typing import Any

from flask import Flask

from .repositories.database import make_session
from .repositories.event_repository import (EventRepository, InMemoryEventRepository,
                                         SqlAlchemyEventRepository)
from .services.event_service import EventService


def create_app(test_config: Mapping[str, Any] | None = None,
               repository: EventRepository | None = None) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    # Signs the CSRF tokens Flask-WTF puts in every form. Set SECRET_KEY in production.
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev")
    app.config["DATABASE_URL"] = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(app.instance_path, 'simcha.db')}")

    if test_config is not None:
        app.config.from_mapping(test_config)

    # The one place that chooses the repository implementation.
    if repository is None:
        if app.config.get("TESTING"):
            repository = InMemoryEventRepository()   # a test can never touch the real database by accident
        else:
            repository = sql_repository(app)
    app.extensions["event_service"] = EventService(repository)

    from .event_routes import bp as events_bp
    from .routes import bp

    app.register_blueprint(bp)
    app.register_blueprint(events_bp)
    return app


def sql_repository(app: Flask) -> SqlAlchemyEventRepository:
    os.makedirs(app.instance_path, exist_ok=True)   # where the default SQLite file lives
    session = make_session(app.config["DATABASE_URL"])
    app.teardown_appcontext(lambda exception: session.remove())   # each request gets a fresh session
    return SqlAlchemyEventRepository(session)
