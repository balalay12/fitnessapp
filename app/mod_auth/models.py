from app import db
from app.models_base import Base

from flask_login import current_user

class User(Base):

    __tablename__ = 'auth_user'

    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(192))
    vk_id = db.Column(db.Integer(), unique=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    photo = db.Column(db.String())
    goal = db.Column(db.String())
    role = db.Column(db.String(), default='user')
    sets = db.relationship('Sets', backref='sets', lazy='dynamic')
    anthropometry = db.relationship('Anthropometry', backref='anthropometry', lazy='dynamic')

    # user trainer
    trainer_id = db.Column(db.Integer, db.ForeignKey('auth_user.id'))

    # fields for trainers
    price = db.Column(db.Integer())
    description = db.Column(db.String())

    def is_authenticated():
        return True

    def is_active():
        return True

    def is_anonymous():
        return False

    @property
    def serialize(self):
        trainer = ''
        if not self.trainer_id is None:
            raw = User.query.get(self.trainer_id)
            trainer = raw.serialize

        return {
            'id': self.id,
            'email': self.email,
            'vk_id': self.vk_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'photo': self.photo,
            # TODO: new model for user roles
            'goal': self.goal,
            'role': self.role,

            # trainer fields
            'price': self.price if self.role == 'trainer' else '',
            'description': self.description if self.role == 'trainer' else '',

            'trainer': trainer
        }

    def serialize_trainer(self, notification=None):
        """
        Serialize trainer info and check if user already make request to trainer
        """

        # TODO: filter by status of notification too
        notify = notification.query.filter_by(
            from_id=current_user.id,
            to_id=self.id
        )

        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'photo': self.photo,
            'price': self.price if self.role == 'trainer' else '',
            'description': self.description if self.role == 'trainer' else '',
            'request': False if notify.count() == 0 else True
        }

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %s %s' % (self.id, self.email)
