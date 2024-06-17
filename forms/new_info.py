from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired
from wtforms.validators import Required
from _datetime import datetime


class InfoForm(FlaskForm):
    name = StringField('Название события', validators=[DataRequired()])
    photo = FileField('Фотография', validators=[FileRequired()])
    date = DateField('Дата рождения', default=datetime.today(), format='%Y-%m-%d')
    submit = SubmitField('Обновить')