from app.db import db
from app.domain.event import Event
from app.models.event_model import EventModel
from app.repositories.event_repository import EventRepository


def to_event(model):
    """EventModel (a database row) -> Event (what the rest of the app uses)."""
    event = Event(model.event_type, model.event_date, model.guest_count, model.budget)
    event.id = model.id
    return event


def copy_to_model(event, model):
    """Copy every field of an Event onto an EventModel."""
    model.event_type = event.event_type
    model.event_date = event.event_date
    model.guest_count = event.guest_count
    model.budget = event.budget


class SqlAlchemyEventRepository(EventRepository):
    """Keeps events in the database.

    Takes and returns Event objects, exactly like InMemoryEventRepository.
    EventModel and db.session never leave this file.
    """

    def add(self, event):
        model = EventModel()
        copy_to_model(event, model)
        db.session.add(model)
        db.session.commit()          # the database assigns model.id here
        event.id = model.id
        return event

    def get(self, event_id):
        model = db.session.get(EventModel, event_id)
        if model is None:
            return None
        return to_event(model)

    def all(self):
        models = db.session.scalars(db.select(EventModel).order_by(EventModel.id))
        return [to_event(model) for model in models]

    def update(self, event_id, event):
        model = db.session.get(EventModel, event_id)
        if model is None:
            return None
        copy_to_model(event, model)
        db.session.commit()
        event.id = event_id
        return event
