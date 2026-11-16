from datetime import date

from flask import Blueprint, current_app, redirect, render_template, url_for

from .ai.ai_provider import AIProviderError
from .forms import EVENT_TYPE_LABELS, ChecklistItemForm, EventForm, SuggestIdeasForm, ToggleItemForm
from .services.checklist_service import ChecklistService
from .services.event_service import EventService

bp = Blueprint("events", __name__, url_prefix="/events")

INVALID_INPUT = "Please enter a valid date, guest count, and budget."


def event_service() -> EventService:
    return current_app.extensions["event_service"]


def checklist_service() -> ChecklistService:
    return current_app.extensions["checklist_service"]


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


def show_event_page(event, ideas=None, ai_error=None, checklist_form=None, checklist_error=None):
    """The event page with its checklist, optionally with AI ideas or a friendly message that there are none."""
    return render_template("events/show.html", event=event, label=EVENT_TYPE_LABELS[event.event_type],
                           days_left=event.days_until_event(date.today()), ideas_form=SuggestIdeasForm(),
                           ideas=ideas, ai_error=ai_error,
                           checklist=checklist_service().items_for_event(event.id),
                           checklist_form=checklist_form or ChecklistItemForm(formdata=None),
                           checklist_error=checklist_error, toggle_form=ToggleItemForm())


@bp.get("/<int:event_id>")
def show_event(event_id):
    event = event_service().get_event(event_id)
    if event is None:
        return render_template("events/not_found.html"), 404
    return show_event_page(event)


@bp.post("/<int:event_id>/ideas")
def suggest_ideas(event_id):
    event = event_service().get_event(event_id)
    if event is None:
        return render_template("events/not_found.html"), 404

    if not SuggestIdeasForm().validate():   # only the CSRF token to check
        return show_event_page(event), 400

    try:
        ideas = current_app.extensions["idea_service"].suggest_ideas(event_id)
    except AIProviderError:
        current_app.logger.exception("AI ideas failed for event %s", event_id)
        return show_event_page(event, ai_error="Ideas are not available right now. Please try again later.")

    return show_event_page(event, ideas=ideas)


@bp.post("/<int:event_id>/checklist")
def add_checklist_item(event_id):
    event = event_service().get_event(event_id)
    if event is None:
        return render_template("events/not_found.html"), 404

    form = ChecklistItemForm()
    if not form.validate():   # only the CSRF token to check; ChecklistItem checks the title
        return show_event_page(event, checklist_form=form), 400

    try:
        checklist_service().add_item(event_id, form.title.data)
    except ValueError as error:
        return show_event_page(event, checklist_form=form, checklist_error=str(error)), 400

    return redirect(url_for("events.show_event", event_id=event_id))


@bp.post("/<int:event_id>/checklist/<int:item_id>/toggle")
def toggle_checklist_item(event_id, item_id):
    if event_service().get_event(event_id) is None:
        return render_template("events/not_found.html"), 404
    if not ToggleItemForm().validate():   # only the CSRF token to check
        return redirect(url_for("events.show_event", event_id=event_id))
    if checklist_service().toggle_item(event_id, item_id) is None:
        return render_template("events/not_found.html"), 404
    return redirect(url_for("events.show_event", event_id=event_id))



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
