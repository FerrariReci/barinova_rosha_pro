from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, SelectField, validators
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField, DateField
from datetime import datetime


class RegisterForm(FlaskForm):
    email = EmailField('Электронная почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    username = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    age = DateField('Дата рождения', default=datetime.today(), format='%d-%m-%Y')
    gender = SelectField("Пол", validators=[validators.InputRequired()], choices=[(0, "Мужской"),
                                                                                  (1, "Женский"),])
    submit = SubmitField('Зарегистрироваться')