from app import db
from app.models_base import Base


class Sets(Base):

    __tablename__ = 'sets'

    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('auth_user.id'))
    repeats = db.relationship('Repeats', cascade=['delete'], backref='repeats', lazy='dynamic')

    def __repr__(self):
        return f"<Set id: {self.id}>"


class Exercises(Base):

    __tablename__ = 'exercises'

    name = db.Column(db.String())
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __repr__(self):
        return f"<Exercise {self.name}>"


class Categories(db.Model):

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    exercises = db.relationship('Exercises', backref='exercises', lazy='dynamic')

    def __repr__(self):
        return f"<Category name {self.name}>"


class Repeats(Base):

    __tablename__ = 'repeats'

    set_id = db.Column(db.Integer, db.ForeignKey('sets.id'))
    weight = db.Column(db.Integer)
    count = db.Column(db.Integer)

    def __repr__(self):
        return f"<Repeat id {self.id}"
