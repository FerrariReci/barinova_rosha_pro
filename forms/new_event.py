from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class EventForm(FlaskForm):
    name = StringField('Название события', validators=[DataRequired()])
    submit = SubmitField('Создать')