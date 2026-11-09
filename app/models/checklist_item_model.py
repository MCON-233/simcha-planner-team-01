from app.db import db


class ChecklistItemModel(db.Model):
    """One row of the checklist_items table.

    Only the SQLAlchemy checklist repository uses this class. Everything else in
    the app works with ChecklistItem, the plain Python class in app/domain/checklist_item.py.
    """

    __tablename__ = "checklist_items"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, nullable=False, default=False)
