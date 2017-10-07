from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField
from wtforms.validators import DataRequired

from .models import *
from sqlalchemy.exc import SQLAlchemyError
from flask_login import current_user


class SetAdd(FlaskForm):

    date = DateField(validators=[
        DataRequired(),
    ])
    exercise = IntegerField(validators=[
        DataRequired(),
    ])


class SetEdit(FlaskForm):

    id = IntegerField(validators=[
        DataRequired(),
    ])
    exercise_id = IntegerField(validators=[
        DataRequired(),
    ])

    def save(self):
        set_instance = Sets.query.get(self.id.data)
        set_instance.exercise_id = self.exercise_id.data
        if not set_instance.user_id == current_user.id:
            return dict(error='Отказано в доступе')
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return dict(error='Не удалось сохранить. Попробуйте позже.')
        return dict(response='ok')


class DeleteForm(FlaskForm):

    id = IntegerField(validators=[
        DataRequired(),
    ])

    def delete_set(self):
        set_instance = Sets.query.get(self.id.data)
        if not set_instance.user_id == current_user.id:
            return dict(error='Отказано в доступе')
        try:
            db.session.delete(set_instance)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return dict(error='Не удалось удалить. Попробуйте позже.')
        return dict(response='ok')

    def delete_rep(self):
        repeat_instance = Repeats.query.get(self.id.data)
        sets_instance = Sets.query.get(repeat_instance.set_id)
        if not sets_instance.user_id == current_user.id:
            return dict(error='Отказано в доступе')
        try:
            db.session.delete(repeat_instance)
            db.session.commit()
        except SQLAlchemyError:
            return dict(error='Не удалось сохранить. Попробуйте позже.')
        return dict(response='ok')


class RepsAdd(FlaskForm):

    weight = IntegerField(validators=[
        DataRequired(),
    ])
    count = IntegerField(validators=[
        DataRequired(),
    ])

    def save(self):
        pass


class RepsAddWithId(FlaskForm):

    id = IntegerField(validators=[
        DataRequired(),
    ])
    weight = IntegerField(validators=[
        DataRequired(),
    ])
    count = IntegerField(validators=[
        DataRequired(),
    ])

    def save(self):
        sets_instance = Sets.query.get(self.id.data)
        if not sets_instance.user_id == current_user.id:
            return dict(error='Отказано в доступе')
        new_rep = Repeats(
            set_id=self.id.data,
            weight=self.weight.data,
            count=self.count.data
        )
        db.session.add(new_rep)
        try:
            db.session.commit()
        except SQLAlchemyError:
            return dict(error='Не удалось сохранить. Попробуйте позже.')
        return dict(response='ok')

    def update(self):
        repeat_instance = Repeats.query.get(self.id.data)
        sets_instance = Sets.query.get(repeat_instance.set_id)
        if not sets_instance.user_id == current_user.id:
            return dict(error='Отказано в доступе')
        repeat_instance.weight = self.weight.data
        repeat_instance.count = self.count.data
        try:
            db.session.commit()
        except SQLAlchemyError:
            return dict(error='Не удалось сохранить. Попробуйте позже.')
        return dict(response='ok')
