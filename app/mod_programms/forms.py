from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired


class ProgrammAdd(FlaskForm):
    name = StringField(validators=[DataRequired(), ])


class ProgrammEdit(FlaskForm):
    id = IntegerField(validators=[DataRequired(), ])
    name = StringField(validators=[DataRequired(), ])


class IdForm(FlaskForm):
    id = IntegerField(validators=[DataRequired(), ])


class ChangeExercise(FlaskForm):
    id = IntegerField(validators=[DataRequired(), ])
    old_exercise = IntegerField(validators=[DataRequired(), ])
    new_exercise = IntegerField(validators=[DataRequired(), ])


class DeleteExercise(FlaskForm):
    id = IntegerField(validators=[DataRequired(), ])
    exercise_id = IntegerField(validators=[DataRequired(), ])