from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField
from wtforms.validators import DataRequired


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


class DeleteForm(FlaskForm):

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
