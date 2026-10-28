from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, IntegerField, SelectChoice, SelectField
from wtforms.validators import InputRequired

EVENT_TYPE_LABELS = {
    "bar_mitzvah": "Bar mitzvah",
    "bat_mitzvah": "Bat mitzvah",
    "vort": "Vort",
    "sheva_brachos": "Sheva brachos",
}


class EventForm(FlaskForm):
    """Reads what the host typed. The rules for a valid event stay in Event."""

    # validate_choice=False: Event decides which types are allowed, so its message is the one shown.
    event_type = SelectField("Type of simcha", validate_choice=False,
                             choices=[SelectChoice(value, label) for value, label in EVENT_TYPE_LABELS.items()])
    event_date = DateField("Date", validators=[InputRequired()])
    guest_count = IntegerField("Number of guests", validators=[InputRequired()])
    budget = FloatField("Budget ($)", validators=[InputRequired()])
