from datetime import date

from flask import Blueprint, current_app, redirect, render_template, url_for

from .forms import EVENT_TYPE_LABELS, EventForm
from .services.event_service import EventService

bp = Blueprint("events", __name__, url_prefix="/events")

INVALID_INPUT = "Please enter a valid date, guest count, and budget."


def event_service() -> EventService:
    return current_app.extensions["event_service"]


@bp.get("")
def list_events():
    return render_template("events/list.html", events=event_service().list_events(),
                           labels=EVENT_TYPE_LABELS)


def show_form(form, error=None, status=200):
    """Show the form, with an error message and the values the host already typed."""
    return render_template("events/new.html", form=form, error=error), status


@bp.get("/new")
def new_event():
    return show_form(EventForm())


@bp.post("")
def create_event():
    form = EventForm()
    if not form.validate():
        return show_form(form, INVALID_INPUT, 400)

    try:
        event = event_service().create_event(form.event_type.data, form.event_date.data,
                                             form.guest_count.data, form.budget.data)
    except ValueError as error:
        return show_form(form, str(error), 400)

    return redirect(url_for("events.show_event", event_id=event.id))


@bp.get("/<int:event_id>")
def show_event(event_id):
    event = event_service().get_event(event_id)
    if event is None:
        return render_template("events/not_found.html"), 404
    return render_template("events/show.html", event=event, label=EVENT_TYPE_LABELS[event.event_type],
                           days_left=event.days_until_event(date.today()))



def show_edit_form(event_id, form, error=None, status=200):
    """Show the edit form, filled in with the event's current values or what the host typed."""
    return render_template("events/edit.html", event_id=event_id, form=form, error=error), status


@bp.get("/<int:event_id>/edit")
def edit_event(event_id):
    event = event_service().get_event(event_id)
    if event is None:
        return render_template("events/not_found.html"), 404
    return show_edit_form(event_id, EventForm(obj=event))


@bp.post("/<int:event_id>/edit")
def update_event(event_id):
    if event_service().get_event(event_id) is None:
        return render_template("events/not_found.html"), 404

    form = EventForm()
    if not form.validate():
        return show_edit_form(event_id, form, INVALID_INPUT, 400)

    try:
        event_service().update_event(event_id, form.event_type.data, form.event_date.data,
                                     form.guest_count.data, form.budget.data)
    except ValueError as error:
        return show_edit_form(event_id, form, str(error), 400)

    return redirect(url_for("events.show_event", event_id=event_id))
