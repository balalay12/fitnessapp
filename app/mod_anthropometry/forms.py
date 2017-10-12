from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField
from wtforms.validators import DataRequired

from app import db
from flask import jsonify
from flask_login import current_user
from .models import Anthropometry
from sqlalchemy.exc import SQLAlchemyError


class BodySizeAdd(FlaskForm):
    neck = FloatField()
    chest = FloatField()
    waist = FloatField()
    forearm = FloatField()
    arm = FloatField()
    hip = FloatField()
    shin = FloatField()

    def save(self):
        new_anthropometry = Anthropometry(
            neck=self.neck.data,
            chest=self.chest.data,
            waist=self.waist.data,
            forearm=self.forearm.data,
            arm=self.arm.data,
            hip=self.hip.data,
            shin=self.shin.data,
            user_id=current_user.id
        )
        db.session.add(new_anthropometry)
        try:
            db.session.commit()
        except SQLAlchemyError:
            return jsonify(error='Не удалось сохранить. Попробуйте позже.')
        return dict(response='ok')


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

    def save(self):
        instance = Anthropometry.query.get(self.id.data)
        if not instance.user_id == current_user.id:
            return dict(error='Отказано в доступе')
        instance.neck = self.neck.data
        instance.chest = self.chest.data
        instance.waist = self.waist.data
        instance.forearm = self.forearm.data
        instance.arm = self.arm.data
        instance.hip = self.hip.data
        instance.shin = self.shin.data
        try:
            db.session.commit()
        except SQLAlchemyError:
            return dict(error='Не удалось сохранить. Попробуйте позже.')
        return dict(response='ok')
