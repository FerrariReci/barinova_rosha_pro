from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeLocalField
from wtforms.validators import DataRequired


class EventForm(FlaskForm):
    name = StringField('Название события', validators=[DataRequired()])
    date_time = DateTimeLocalField('Дата и время события', format='%Y-%m-%dT%H:%M',
                                   validators=[DataRequired()])
    place = StringField('Место проведения', validators=[DataRequired()])
    text = StringField('Описание события', validators=[DataRequired()])
    category = StringField('Доступные категории(id)', validators=[DataRequired()])
    distance = StringField('Дистанции', validators=[DataRequired()])
    submit = SubmitField('Создать')