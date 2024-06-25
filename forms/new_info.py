from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from wtforms.validators import Required
from _datetime import datetime


class InfoForm(FlaskForm):
    name = StringField('Название события', validators=[DataRequired()])
    date = DateField('Дата', default=datetime.today(), format='%Y-%m-%d')