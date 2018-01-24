from app import db


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

    @property
    def serialize(self):
        notification_status = NotificationStatus.query.get(self.status)
        return {
            'id': self.id,
            'from': self.from_id,
            'to': self.to_id,
            'message': self.message,
            'status': str(notification_status)
        }
