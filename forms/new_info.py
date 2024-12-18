from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired
from _datetime import datetime


class InfoForm(FlaskForm):
    name = StringField('Название события', validators=[DataRequired()])
    date = DateField('Дата', default=datetime.today(), format='%Y-%m-%d')