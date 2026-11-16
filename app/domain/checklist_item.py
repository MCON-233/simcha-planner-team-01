MAX_TITLE_LENGTH = 200


class ChecklistItem:
    def __init__(self, event_id, title, done=False):
        """A new checklist item. Its title is trimmed and must not be blank."""
        title = (title or "").strip()
        self._validate(title)
        self.event_id = event_id
        self.title = title
        self.done = done
        self.id = None

    @classmethod
    def restore(cls, item_id, event_id, title, done):
        item = cls.__new__(cls)
        item.id = item_id
        item.event_id = event_id
        item.title = title
        item.done = done
        return item

    @staticmethod
    def _validate(title):
        if not title:
            raise ValueError("Checklist item needs a title")
        if len(title) > MAX_TITLE_LENGTH:
            raise ValueError(f"Checklist item must be {MAX_TITLE_LENGTH} characters or fewer")
