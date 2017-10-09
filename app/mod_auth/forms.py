from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length

from app import db, bcrypt
from flask_login import login_user
from .models import User
from sqlalchemy.exc import SQLAlchemyError


class RegistrationForm(FlaskForm):

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

    def save(self):
        check_user_email = User.query.filter_by(email=self.email.data).first()
        if check_user_email is not None:
            return dict(error='Пользователь с такой почтой уже зарегестрирован')
        user = User(
            email=self.email.data,
            first_name=self.first_name.data,
            last_name=self.last_name.data,
            password=bcrypt.generate_password_hash(self.password.data)
        )
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return dict(error='Не удалось сохранить. Попробуйте позже.')
        return dict(response='ok')


class LoginForm(FlaskForm):

    email = StringField('Email', validators=[
        DataRequired("Поле эл. почты обязательно для заполнения."),
        Email('Введите корректный адрес эл. почты.')])
    password = PasswordField('Password', validators=[
        DataRequired('Поле пароля обязательно.')
        ])

    def save(self):
        try:
            user = User.query.filter_by(email=self.email.data).first()
        except SQLAlchemyError as e:
            return dict(error='Ошибка.')
        if user is None:
            return dict(error='Пользователь не найден.')
        if bcrypt.check_password_hash(user.password, self.password.data):
            login_user(user)
            return dict(response='ok')
        return dict(error='Не правильно введен пароль.')
