from app.db import db
from app.domain.checklist_item import ChecklistItem
from app.models.checklist_item_model import ChecklistItemModel
from app.repositories.checklist_repo import ChecklistRepository


def to_item(model):
    """ChecklistItemModel (a database row) -> ChecklistItem (what the rest of the app uses)."""
    return ChecklistItem.restore(model.id, model.event_id, model.title, model.done)


def copy_to_model(item, model):
    """Copy every field of a ChecklistItem onto a ChecklistItemModel."""
    model.event_id = item.event_id
    model.title = item.title
    model.done = item.done


class SqlAlchemyChecklistRepository(ChecklistRepository):
    """Keeps checklist items in the database.

    Takes and returns ChecklistItem objects, exactly like InMemoryChecklistRepository.
    ChecklistItemModel and db.session never leave this file.
    """

    def add(self, item):
        model = ChecklistItemModel()
        copy_to_model(item, model)
        db.session.add(model)
        db.session.commit()          # the database assigns model.id here
        item.id = model.id
        return item

    def get(self, item_id):
        model = db.session.get(ChecklistItemModel, item_id)
        if model is None:
            return None
        return to_item(model)

    def for_event(self, event_id):
        models = db.session.scalars(
            db.select(ChecklistItemModel)
            .where(ChecklistItemModel.event_id == event_id)
            .order_by(ChecklistItemModel.id)
        )
        return [to_item(model) for model in models]

    def update(self, item_id, item):
        model = db.session.get(ChecklistItemModel, item_id)
        if model is None:
            return None
        copy_to_model(item, model)
        db.session.commit()
        item.id = item_id
        return item
