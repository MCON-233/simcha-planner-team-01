from flask import Blueprint, Response, jsonify, render_template

bp = Blueprint("main", __name__)


@bp.get("/")
def index() -> str:
    return render_template("index.html")


@bp.get("/health")
def health() -> tuple[Response, int]:
    """Return a small response for automated health checks."""
    return jsonify(status="ok"), 200
