from app import db
from app.models_base import Base


class Anthropometry(Base):

    __tablename__ = 'anthropometry'

    user_id = db.Column(db.Integer, db.ForeignKey('auth_user.id'))
    weight = db.Column(db.Float)
    # шея
    neck = db.Column(db.Float)
    chest = db.Column(db.Float)
    # талия
    waist = db.Column(db.Float)
    # предплечье
    forearm = db.Column(db.Float)
    arm = db.Column(db.Float)
    # бедро
    hip = db.Column(db.Float)
    # голень
    shin = db.Column(db.Float)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'date': self.date_created,
            'weight': self.weight,
            'neck': self.neck,
            'chest': self.chest,
            'waist': self.waist,
            'forearm': self.forearm,
            'arm': self.arm,
            'hip': self.hip,
            'shin': self.shin
        }
