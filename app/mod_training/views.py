import calendar

from collections import defaultdict
from flask import (
    abort,
    Blueprint,
    jsonify,
    request
)
from trafaret import DataError
from flask_login import current_user, login_required
from .models import *
from .validators import *
from app.mod_programms.models import Programm
from app.mod_auth.models import User
from app.mod_notifications.models import Notifications
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

mod_training = Blueprint('training', __name__, url_prefix='/training')


@mod_training.route('/categories', methods=['GET'])
def categories():
    categories = Categories.query.all()
    return jsonify(categories=[category.serialize for category in categories])


@mod_training.route('/exercises', methods=['GET'])
def exercises():
    exercises = Exercises.query.filter()
    return jsonify(exercises=[exercise.serialize for exercise in exercises])


@mod_training.route('/sets', methods=['GET'])
@login_required
def sets():
    client_id = request.args.get('id')
    month = request.args.get('month')
    year = request.args.get('year')

    if not month and not year:
        dates = _get_dates(datetime.today().month, datetime.today().year)
    else:
        dates = _get_dates(month, year)
    data = defaultdict(list)

    # if client_id exists - its mean we get request from trainer
    # and we need to find client of trainer
    # TODO add test
    if client_id:
        client = User.query.get(int(client_id))
        if client is None:
            return jsonify(error='Клиент не найден')
        if not client.trainer_id == current_user.id:
            return jsonify(error='Отказано в доступе')
        sets = [sets.serialize for sets in client.sets.filter(
            Sets.date >= dates['start'],
            Sets.date <= dates['end']
        ).all()]
    else:
        sets = [sets.serialize for sets in current_user.sets.filter(
            Sets.date >= dates['start'],
            Sets.date <= dates['end']
        ).all()]
    for item in sets:
        data[item['date']].append(item)
    return jsonify(sets=data)


@mod_training.route('/set/add', methods=['POST'])
@login_required
def set_add():
    data = request.get_json(force=True)
    if 'training' not in data:
        abort(400)

    notification = False
    client_id = data.get('id')
    if client_id:
        client = User.query.get(int(client_id))
        if client is None:
            return jsonify(error='Клиент не найден')
        if not client.trainer_id == current_user.id:
            return jsonify(error='Отказано в доступе')
        user = client
        notification = True
    else:
        user = current_user

    for training in data['training']:
        try:
            checking_data = add_set_validator.check(training)
        except DataError:
            return jsonify(error='Проверьте введеные данные!')
        new_set = Sets(
            date=datetime.strptime(checking_data['date'], '%Y-%m-%d'),
            exercise_id=checking_data['exercise'],
            user_id=user.id
        )
        db.session.add(new_set)
        db.session.flush()
        for reps in checking_data['sets']:
            new_reps = Repeats(
                set_id=new_set.id,
                weight=reps['weight'],
                count=reps['count']
            )
            db.session.add(new_reps)
            db.session.flush()

    # уведомление для пользователя о добавлении тренировки тренером
    if notification:
        user_notification = Notifications(
            from_id=current_user.id,
            to_id=client_id,
            message='Ваш тренер добавил Вам тренировку на '
                    + checking_data['date']
                    + ' число'
        )
        db.session.add(user_notification)
        db.session.flush()

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify(error='Что-то пошло не так.')
    return '', 200


@mod_training.route('/set/edit', methods=['POST'])
@login_required
def edit_set():
    data = request.get_json(force=True)
    try:
        checking_data = edit_set_validator.check(data)
    except DataError:
        return jsonify(error='Проверьте введеные данные!')
    set_instance = Sets.query.get(checking_data['id'])
    if set_instance is None:
        return jsonify(error='Подхода с таким ID не найдено')
    set_instance.exercise_id = checking_data['exercise_id']
    if not set_instance.user_id == current_user.id:
        return jsonify(error='Отказано в доступе')
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify(error='Не удалось сохранить. Попробуйте позже.')
    return '', 200


@mod_training.route('/planning', methods=['POST'])
@login_required
def planning_set():
    data = request.get_json(force=True)
    try:
        checking_data = planning_validator.check(data)
    except DataError:
        return jsonify(error='Проверьте введеные данные!')
    programm_instance = Programm.query.get(checking_data['programm_id'])
    if programm_instance is None:
        return jsonify(error='Программы с таким ID не найдено')
    for exercise in programm_instance.exercise:
        new_set = Sets(
            date=datetime.strptime(checking_data['date'], '%Y-%m-%d'),
            exercise_id=exercise.id,
            user_id=current_user.id
        )
        db.session.add(new_set)
        db.session.flush()
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify(error='Что-то пошло не так.')
    return jsonify(response='ok')


@mod_training.route('/set/delete/<id>', methods=['DELETE'])
@login_required
def delete_set(id):
    try:
        set_id = t.Int(gt=0).check(id)
    except DataError:
        return jsonify(error='Проверьте введеные данные!')
    set_instance = Sets.query.get(set_id)
    if set_instance is None:
        return jsonify(error='Подхода с таким ID не найдено')
    if not set_instance.user_id == current_user.id:
        return jsonify(error='Отказано в доступе')
    try:
        db.session.delete(set_instance)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify(error='Не удалось удалить. Попробуйте позже.')
    return '', 200


@mod_training.route('/repeat/add', methods=['POST'])
@login_required
def add_repeat():
    data = request.get_json(force=True)
    try:
        checking_data = add_repeat_validator.check(data)
    except DataError:
        return jsonify(error='Проверьте введеные данные!')
    sets_instance = Sets.query.get(checking_data['id'])
    if sets_instance is None:
        return jsonify(error='Подхода с таким ID не найдено')
    if not sets_instance.user_id == current_user.id:
        return jsonify(error='Отказано в доступе')
    new_rep = Repeats(
        set_id=sets_instance.id,
        weight=checking_data['weight'],
        count=checking_data['count']
    )
    db.session.add(new_rep)
    try:
        db.session.commit()
    except SQLAlchemyError:
        return jsonify(error='Не удалось сохранить. Попробуйте позже.')
    return jsonify(response='ok')


@mod_training.route('/repeat/edit', methods=['POST'])
@login_required
def edit_repeat():
    data = request.get_json(force=True)
    try:
        checking_data = add_repeat_validator.check(data)
    except DataError:
        return jsonify(error='Проверьте введеные данные!')
    repeat_instance = Repeats.query.get(checking_data['id'])
    if repeat_instance is None:
        return jsonify(error='Повтора с таким ID не найдено')
    sets_instance = Sets.query.get(repeat_instance.set_id)
    if not sets_instance.user_id == current_user.id:
        return jsonify(error='Отказано в доступе')
    repeat_instance.weight = checking_data.get('weight')
    repeat_instance.count = checking_data.get('count')
    try:
        db.session.commit()
    except SQLAlchemyError:
        return jsonify(error='Не удалось сохранить. Попробуйте позже.')
    return '', 200


@mod_training.route('/repeat/delete/<id>', methods=['DELETE'])
@login_required
def delete_repeat(id):
    try:
        repeat_id = t.Int(gt=0).check(id)
    except DataError:
        return jsonify(error='Проверьте введеные данные!')
    repeat_instance = Repeats.query.get(repeat_id)
    if repeat_instance is None:
        return jsonify(error='Повтора с таким ID не найдено')
    sets_instance = Sets.query.get(repeat_instance.set_id)
    if not sets_instance.user_id == current_user.id:
        return jsonify(error='Отказано в доступе')
    try:
        db.session.delete(repeat_instance)
        db.session.commit()
    except SQLAlchemyError:
        return jsonify(error='Не удалось сохранить. Попробуйте позже.')
    return '', 200


def _get_dates(month, year):
    last_day = calendar.monthrange(int(year), int(month))[1]
    start = datetime(year=int(year), month=int(month), day=1)
    end = datetime(year=int(year), month=int(month), day=last_day)
    return {'start': start, 'end': end}
