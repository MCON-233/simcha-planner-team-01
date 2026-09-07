from collections.abc import Mapping
from typing import Any

from flask import Flask


def create_app(test_config: Mapping[str, Any] | None = None) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)

    if test_config is not None:
        app.config.from_mapping(test_config)

    from .routes import bp

    app.register_blueprint(bp)
    return app
