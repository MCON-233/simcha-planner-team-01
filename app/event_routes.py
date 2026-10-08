from datetime import date

from flask import Blueprint, current_app, redirect, render_template, request, url_for
from werkzeug.wrappers import Response

from .services.event_service import EventService

bp = Blueprint("events", __name__, url_prefix="/events")

EVENT_TYPE_LABELS: dict[str, str] = {
    "bar_mitzvah": "Bar mitzvah",
    "bat_mitzvah": "Bat mitzvah",
    "vort": "Vort",
    "sheva_brachos": "Sheva brachos",
    "community_dinner": "Community dinner",
    "birthday": "Birthday celebration",
}


def event_service() -> EventService:
    return current_app.extensions["event_service"]


def show_form(error: str | None = None, status: int = 200) -> tuple[str, int]:
    html = render_template(
        "events/new.html", event_types=EVENT_TYPE_LABELS, form=request.form, error=error
    )
    return html, status


@bp.get("/new")
def new_event() -> tuple[str, int]:
    return show_form()


@bp.post("")
def create_event() -> Response | tuple[str, int]:
    form = request.form
    try:
        event_date = date.fromisoformat(form["event_date"])
        guest_count = int(form["guest_count"])
        budget = float(form["budget"])
    except (KeyError, ValueError):
        return show_form("Please enter a valid date, guest count, and budget.", 400)

    try:
        event = event_service().create_event(
            form.get("event_type", ""),
            event_date,
            guest_count,
            budget,
            venue=form.get("venue", "").strip(),
            theme=form.get("theme", "").strip(),
        )
    except ValueError as error:
        return show_form(str(error), 400)

    return redirect(url_for("events.dashboard", event_id=event.id))


@bp.get("/<int:event_id>")
def dashboard(event_id: int) -> tuple[str, int]:
    event = event_service().get_event(event_id)
    if event is None:
        return render_template("events/not_found.html"), 404
    return (
        render_template(
            "events/dashboard.html",
            event=event,
            event_type_label=EVENT_TYPE_LABELS[event.event_type],
            days_left=event.days_until(date.today()),
        ),
        200,
    )
