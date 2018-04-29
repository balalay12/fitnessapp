import trafaret as t

from flask import (
    Blueprint,
    jsonify,
    request
)
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError

from .models import *
from app.mod_auth.models import User


mod_notifications = Blueprint('notifications', __name__, url_prefix='/notifications')


@mod_notifications.route('/', methods=['GET'])
@login_required
def get_notifications():
    """
    Get all notifications for current user
    """

    # TODO: make datetime field in DB and order notifications
    notifications = Notifications.query.filter_by(to_id=current_user.id)
    return jsonify(notifications=[notification.serialize for notification in notifications])


@mod_notifications.route('/new', methods=['GET'])
@login_required
def get_new_notifications():
    """
    Get new notifications for current user
    """

    notifications = []
    for x in Notifications.query.filter_by(to_id=current_user.id, new=True):
        notifications.append(x.serialize)
        x.new = False
    db.session.commit()
    return jsonify(notifications=notifications)


@mod_notifications.route('/create_add_trainer_notification', methods=['POST'])
@login_required
def create_add_trainer_notification():
    """
    Creating notifications for current user and also for trainer
    """

    trainer_id_validator = t.Dict({
        t.Key('id') >> 'id': t.Int(gt=0)
    })

    data = request.get_json(force=True)
    try:
        cheking_data = trainer_id_validator.check(data)
    except t.DataError:
        return jsonify(error='Проверьте введеные данные!')

    try:
        trainer_instance = User.query.filter_by(id=cheking_data['id']).first()
    except SQLAlchemyError:
        return jsonify(error='Произошла ошибка. Попробуйте позже.')

    if trainer_instance.role != 'trainer':
        return jsonify(error='Вы можете подавать заявку только тренерам.')

    # create notification for user
    note_for_user = Notifications(
        from_id=current_user.id,
        to_id=current_user.id,
        message='Вы отправили зявку тренеру '
                + trainer_instance.first_name
                + ' '
                + trainer_instance.last_name
    )

    # notification for trainer
    note_for_trainer = Notifications(
        from_id=current_user.id,
        to_id=cheking_data['id'],
        message='Пользователь '
                + current_user.first_name
                + ' '
                + current_user.last_name
                + ' отправил Вам зявку, чтобы стать вашим клиентом',
        need_confirm=True
    )

    db.session.add(note_for_user)
    db.session.add(note_for_trainer)

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify(error='Не удалось сохранить. Попробуйте позже.')
    return '', 200


@mod_notifications.route('/accept/<id>', methods=['GET',])
@login_required
def accept_notification(id):
    if current_user.role != 'trainer':
        return jsonify(error='Вы не являетесь тренером.')

    try:
        notification_id = t.Int().check(id)
    except t.DataError:
        return jsonify(error='Проверьте введеные данные!')
    notification = Notifications.query.get(notification_id)
    if notification is None:
        return jsonify(error='Уведомление не найдено.')
    if notification.to_id != current_user.id:
        return jsonify(error='Отказано в доступе')

    # update notification status and confirm
    notification.status = 1
    notification.need_confirm = False

    # create notification for sender
    note = Notifications(
        from_id=current_user.id,
        to_id=notification.from_id,
        message='Пользователь '
                + current_user.first_name + ' '
                + current_user.last_name
                + ' прнял вашу заявку'
    )
    db.session.add(note)

    # set trainer for sender
    sender = User.query.get(notification.from_id)
    sender.trainer_id = current_user.id

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify(error='Не удалось сохранить. Попробуйте позже.')
    return '', 200


@mod_notifications.route('/decline/<id>', methods=['GET',])
@login_required
def decline_notification(id):
    if current_user.role != 'trainer':
        return jsonify(error='Вы не являетесь тренером.')

    try:
        notification_id = t.Int().check(id)
    except t.DataError:
        return jsonify(error='Проверьте введеные данные!')
    notification = Notifications.query.get(notification_id)
    if notification is None:
        return jsonify(error='Уведомление не найдено.')
    if notification.to_id != current_user.id:
        return jsonify(error='Отказано в доступе')
    # update notification status and confirm
    # 2 equal decline
    notification.status = 2
    notification.need_confirm = False

    # create notification for sender
    note = Notifications(
        from_id=current_user.id,
        to_id=notification.from_id,
        message='Пользователь '
                + current_user.first_name + ' '
                + current_user.last_name

                + ' отклонил вашу заявку'
    )
    db.session.add(note)

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify(error='Не удалось сохранить. Попробуйте позже.')
    return '', 200
