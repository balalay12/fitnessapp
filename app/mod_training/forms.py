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


class PlanningSetForm(FlaskForm):
    programm_id = IntegerField(validators=[
        DataRequired(),
    ])
    date = DateField(validators=[
        DataRequired(),
    ])


class SetEdit(FlaskForm):

    id = IntegerField(validators=[
        DataRequired(),
    ])
    exercise_id = IntegerField(validators=[
        DataRequired(),
    ])


class IdForm(FlaskForm):

    id = IntegerField(validators=[
        DataRequired(),
    ])


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
