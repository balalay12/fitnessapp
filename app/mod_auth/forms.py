from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class RegistrationForm(FlaskForm):
    class Meta:
        csrf = False

    email = StringField('Email', validators=[
        DataRequired("Поле эл. почты обязательно для заполнения."), 
        Email('Введите корректный адрес эл. почты.')])
    password = PasswordField('Password', validators=[
        DataRequired('Поле пароля обязательно.'),
        Length(min=8, message="Пароль должен быть не менее 8 символов.")
        ])
    first_name = StringField('First Name', validators=[
        DataRequired('Поле пароля обязательно.'),
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired('Поле пароля обязательно.'),
    ])


class LoginForm(FlaskForm):
    class Meta:
        csrf = False

    email = StringField('Email', validators=[
        DataRequired("Поле эл. почты обязательно для заполнения."),
        Email('Введите корректный адрес эл. почты.')])
    password = PasswordField('Password', validators=[
        DataRequired('Поле пароля обязательно.')
        ])
