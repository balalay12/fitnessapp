from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField
from wtforms.validators import DataRequired


class SetAdd(FlaskForm):
    class Meta:
        csrf = False

    date = DateField(validators=[
        DataRequired(),
    ])
    exercise = IntegerField(validators=[
        DataRequired(),
    ])


class SetEdit(FlaskForm):
    class Meta:
        csrf = False

    id = IntegerField(validators=[
        DataRequired(),
    ])
    exercise_id = IntegerField(validators=[
        DataRequired(),
    ])


class DeleteForm(FlaskForm):
    class Meta:
        csrf = False

    id = IntegerField(validators=[
        DataRequired(),
    ])


class RepsAdd(FlaskForm):
    class Meta:
        csrf = False

    weight = IntegerField(validators=[
        DataRequired(),
    ])
    count = IntegerField(validators=[
        DataRequired(),
    ])


class RepsAddWithId(FlaskForm):
    class Meta:
        csrf = False

    id = IntegerField(validators=[
        DataRequired(),
    ])
    weight = IntegerField(validators=[
        DataRequired(),
    ])
    count = IntegerField(validators=[
        DataRequired(),
    ])
