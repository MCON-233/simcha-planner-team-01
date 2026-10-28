from app.db import db


class EventModel(db.Model):
    """One row of the events table.

    Only the SQLAlchemy repository uses this class. Everything else in the app
    works with Event, the plain Python class in app/domain/event.py.
    """

    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(40), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    guest_count = db.Column(db.Integer, nullable=False)
    budget = db.Column(db.Float, nullable=False)
