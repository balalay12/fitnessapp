from app import db


class Sets(db.Model):

    __tablename__ = 'sets'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('auth_user.id'))
    repeats = db.relationship('Repeats', cascade=['delete'], backref='repeats', lazy='dynamic')

    @property
    def serialize(self):
        exercise = Exercises.query.get(self.exercise_id)
        reps = Repeats.query.filter_by(set_id=self.id)
        repeats = []
        for rep in reps:
            repeats.append(rep.serialize)
        return {
            'id': self.id,
            'date': self.date.strftime("%Y-%m-%d"),
            'exercise': exercise.serialize,
            'repeats': repeats
        }

    def __repr__(self):
        return "<Set id: %s>" % (self.id)


class Exercises(db.Model):

    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    @property
    def serialize(self):
        category = Categories.query.get(self.category_id)
        return {
            'id': self.id,
            'name': self.name,
            'category': category.serialize
        }

    def __repr__(self):
        return "<Exercise: %s>" % (self.name)


class Categories(db.Model):

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    exercises = db.relationship('Exercises', backref='exercises', lazy='dynamic')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def __repr__(self):
        return "<Category name: %s>" % (self.name)


class Repeats(db.Model):

    __tablename__ = 'repeats'

    id = db.Column(db.Integer, primary_key=True)
    set_id = db.Column(db.Integer, db.ForeignKey('sets.id'))
    weight = db.Column(db.Integer)
    count = db.Column(db.Integer)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'set_id': self.set_id,
            'weight': self.weight,
            'count': self.count
        }

    def __repr__(self):
        return "<Repeat id: %s" % (self.id)

