from app import db
from app.models_base import Base


class User(Base):

    __tablename__ = 'auth_user'

    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(192))
    vk_id = db.Column(db.Integer(), unique=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    photo = db.Column(db.String())
    sets = db.relationship('Sets', backref='sets', lazy='dynamic')

    def is_authenticated():
        return True

    def is_active():
        return True

    def is_anonymous():
        return False

    @property
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'vk_id': self.vk_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'photo': self.photo
        }

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %s %s' % (self.id, self.email)
