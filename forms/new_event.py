from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired
from wtforms.validators import Required


class EventForm(FlaskForm):
    name = StringField('Название события', validators=[DataRequired()])
    date_time = DateTimeLocalField('Дата и время события', format='%Y-%m-%dT%H:%M',
                                   validators=[Required()])
    place = StringField('Место проведения', validators=[DataRequired()])
    text = TextField('Описание события', validators=[DataRequired()])
    submit = SubmitField('Создать')