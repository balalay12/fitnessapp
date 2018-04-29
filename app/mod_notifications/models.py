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
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

    @property
    def serialize(self):
        from_instance = User.query.get(self.from_id)
        to_instance = User.query.get(self.to_id)

        status = ''
        if not self.status is None:
            status = NotificationStatus.query.get(self.status)

        return {
            'id': self.id,
            'from': from_instance.serialize,
            'to': to_instance.serialize,
            'message': self.message,
            'status': str(status),
            'need_confirm': self.need_confirm,
            # TODO: need to return timestamp for return actual user time
            'date': self.date.strftime('%d.%m.%Y %H:%M')
        }
