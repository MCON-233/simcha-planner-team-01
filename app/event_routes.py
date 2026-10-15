from datetime import date

from flask import Blueprint, current_app, render_template

from .services.event_service import EventService

bp = Blueprint("events", __name__, url_prefix="/events")

EVENT_TYPE_LABELS = {
    "bar_mitzvah": "Bar mitzvah",
    "bat_mitzvah": "Bat mitzvah",
    "vort": "Vort",
    "sheva_brachos": "Sheva brachos",
}


def event_service() -> EventService:
    return current_app.extensions["event_service"]


@bp.get("")
def list_events():
    return render_template("events/list.html", events=event_service().list_events(),
                           labels=EVENT_TYPE_LABELS)


@bp.get("/<int:event_id>")
def show_event(event_id):
    event = event_service().get_event(event_id)
    if event is None:
        return render_template("events/not_found.html"), 404
    return render_template("events/show.html", event=event, label=EVENT_TYPE_LABELS[event.event_type],
                           days_left=event.days_until_event(date.today()))
