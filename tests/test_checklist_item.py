import pytest


from app.domain.checklist_item import ChecklistItem


def test_checklist_item_keeps_its_details():
    item = ChecklistItem(event_id=1, title="Book venue", done=False)
    assert item.event_id == 1
    assert item.title == "Book venue"
    assert item.done is False

def test_new_checklist_item_has_no_id_yet():
    item = ChecklistItem(event_id=1, title="Book venue", done=False)
    assert item.id is None

def test_checklist_item_restore():
    item = ChecklistItem.restore(item_id=1, event_id=1, title="Book venue", done=True)
    assert item.id == 1
    assert item.event_id == 1
    assert item.title == "Book venue"
    assert item.done is True

def test_checklist_item_restore_with_false_done():
    item = ChecklistItem.restore(item_id=2, event_id=1, title="Send invitations", done=False)
    assert item.id == 2
    assert item.event_id == 1
    assert item.title == "Send invitations"
    assert item.done is False

def test_checklist_item_restore_with_true_done():
    item = ChecklistItem.restore(item_id=3, event_id=1, title="Hire photographer", done=True)
    assert item.id == 3
    assert item.event_id == 1
    assert item.title == "Hire photographer"
    assert item.done is True


def test_title_is_trimmed():
    assert ChecklistItem(event_id=1, title="  Book venue  ").title == "Book venue"


def test_title_cannot_be_blank():
    with pytest.raises(ValueError, match="Checklist item needs a title"):
        ChecklistItem(event_id=1, title="   ")


def test_title_cannot_be_too_long():
    with pytest.raises(ValueError, match="200 characters or fewer"):
        ChecklistItem(event_id=1, title="x" * 201)


def test_title_of_200_characters_is_accepted():
    assert len(ChecklistItem(event_id=1, title="x" * 200).title) == 200
