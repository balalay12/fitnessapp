from app import db
from app.mod_auth.models import User

class NotificationStatus(db.Model):

    __tablename__ = 'notification_status'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String())

    def __repr__(self):
        return '%s' % self.status


class Notifications(db.Model):

    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    from_id = db.Column(db.Integer, db.ForeignKey('auth_user.id'))
    to_id = db.Column(db.Integer, db.ForeignKey('auth_user.id'))
    message = db.Column(db.String())
    status = db.Column(db.Integer, db.ForeignKey('notification_status.id'))
    need_confirm = db.Column(db.Boolean, default=False)
    new = db.Column(db.Boolean, default=True)

    @property
    def serialize(self):
        from_instance = User.query.get(self.from_id)
        to_instance = User.query.get(self.to_id)

        # notification_status = NotificationStatus.query.get(self.status)
        return {
            'id': self.id,
            'from': from_instance.serialize,
            'to': to_instance.serialize,
            'message': self.message,
            # 'status': str(notification_status),
            'need_confirm': self.need_confirm
        }
