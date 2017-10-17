from app import db
from app.models_base import Base


exercise = db.Table(
    'exercise',
     db.Column('programm_id', db.Integer, db.ForeignKey('programm.id'), primary_key=True),
     db.Column('exercise_id', db.Integer, db.ForeignKey('exercises.id'), primary_key=True)
)


class Programm(Base):

    __tablename__ = 'programm'

    user_id = db.Column(db.Integer, db.ForeignKey('auth_user.id'))
    name = db.Column(db.Text)
    exercise = db.relationship('Exercises', secondary=exercise, lazy='subquery',
                                backref=db.backref('programm', lazy=True))
