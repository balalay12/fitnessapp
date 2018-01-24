from flask import (
    Blueprint,
    jsonify,
    request
)
from flask.views import MethodView

from .models import *


mod_notifications = Blueprint('notifications', __name__, url_prefix='/notifications')


class NotificationsAPI(MethodView):

    def get(self, notification_id):
        if notification_id is None:
            notifications = Notifications.query.all()
            return jsonify(notifications=[notification.serialize for notification in notifications])
        else:
            pass


notification_view = NotificationsAPI.as_view('notification_api')
mod_notifications.add_url_rule('/', defaults={'notification_id': None},
                               view_func=notification_view, methods=['GET',])
