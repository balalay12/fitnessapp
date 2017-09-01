from app import db


class Base(db.Model):
    
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


class User(Base):

    __tablename__ = 'auth_user'

    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(192))
    vk_id = db.Column(db.Integer(), unique=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))

    # def __init__(self, email, vk_id=None, first_name=None, last_name=None, password=None):
    #     self.email = email
    #     self.password = password
    #     self.first_name = first_name
    #     self.last_name = last_name
    #     self.vk_id = vk_id

    def is_authenticated():
        return True

    def is_active():
        return True

    def is_anonymous():
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %s %s' % (self.id, self.email)
