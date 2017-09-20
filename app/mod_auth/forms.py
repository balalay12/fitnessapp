from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class RegistrationForm(FlaskForm):
    login = StringField('Login', validators=[
        DataRequired("Поле логина обязательно для заполнения."),])
    email = StringField('Email', validators=[
        DataRequired("Поле эл. почты обязательно для заполнения."), 
        Email('Введите корректный адрес эл. почты.')])
    password = PasswordField('Password', validators=[
        DataRequired('Поле пароля обязательно.'),
        Length(min=8, message="Пароль должен быть не менее 8 символов.")
        ])


class LoginForm(FlaskForm):
    login = StringField('Login', validators=[
        DataRequired("Поле логина обязательно для заполнения."),])
    password = PasswordField('Password', validators=[
        DataRequired('Поле пароля обязательно.')
        ])
