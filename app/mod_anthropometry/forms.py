from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField
from wtforms.validators import DataRequired


class BodySizeAdd(FlaskForm):
    neck = FloatField()
    chest = FloatField()
    waist = FloatField()
    forearm = FloatField()
    arm = FloatField()
    hip = FloatField()
    shin = FloatField()


class BodySizeEdit(FlaskForm):
    id = IntegerField(validators=[
        DataRequired(),
    ])
    neck = FloatField()
    chest = FloatField()
    waist = FloatField()
    forearm = FloatField()
    arm = FloatField()
    hip = FloatField()
    shin = FloatField()
