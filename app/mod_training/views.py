import calendar

from collections import defaultdict
from flask import (
    abort,
    Blueprint,
    jsonify,
    request
)
from flask_login import current_user
from .models import *
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

mod_api = Blueprint('api', __name__, url_prefix='/api')


@mod_api.route('/categories', methods=['GET'])
def categories():
    categories = Categories.query.all()
    return jsonify(categories=[category.serialize for category in categories])


@mod_api.route('/exercises', methods=['GET'])
def exercises():
    exercises = Exercises.query.filter()
    return jsonify(exercises=[exercise.serialize for exercise in exercises])


@mod_api.route('/sets', methods=['GET'])
def sets():
    dates = _get_dates(datetime.today().month, datetime.today().year)
    data = defaultdict(list)
    sets = [sets.serialize for sets in current_user.sets.filter(
        Sets.date >= dates['start'],
        Sets.date <= dates['end']
    ).all()]
    for item in sets:
        data[item['date']].append(item)
    return jsonify(sets=data)


@mod_api.route('/set_by_date/<month>/<year>', methods=['GET'])
def sets_by_date(month, year):
    dates = _get_dates(month, year)
    data = defaultdict(list)
    sets = [sets.serialize for sets in current_user.sets.filter(
        Sets.date >= dates['start'],
        Sets.date <= dates['end']
    ).all()]
    for item in sets:
        data[item['date']].append(item)
    return jsonify(sets=data)


@mod_api.route('/set/add', methods=['POST'])
def set_add():
    if not request.json \
       or 'train' not in request.json:
        abort(400)
    for train in request.json['train']:
        new_set = Sets(
            date=datetime.strptime(train['date'], '%Y-%m-%d'),
            exercise_id=train['exercise']['id'],
            user_id=current_user.id
        )
        db.session.add(new_set)
        db.session.flush()
        for reps in train['sets']:
            new_reps = Repeats(
                set_id=new_set.id,
                weight=reps['weight'],
                count=reps['count']
            )
            db.session.add(new_reps)
            db.session.flush()
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        print('error ->', e)
        return jsonify(error='Что-то пошло не так.')
    return '', 200


@mod_api.route('/set/edit', methods=['POST'])
def edit_set():
    if not request.json \
       or 'id' not in request.json \
       or 'exercise_id' not in request.json:
        abort(400)
    set_instance = Sets.query.get(int(request.json['id']))
    set_instance.exercise_id = request.json['exercise_id']
    if not set_instance.user_id == current_user.id:
        return jsonify(error='Отказано в доступе')
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify(error='Не удалось сохранить. Попробуйте позже.')
    return '', 200


@mod_api.route('/set/delete', methods=['POST'])
def delete_set():
    if not request.json \
       or 'id' not in request.json:
        abort(400)
    set_instance = Sets.query.get(int(request.json['id']))
    if not set_instance.user_id == current_user.id:
        return jsonify(error='Отказано в доступе')
    try:
        db.session.delete(set_instance)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify(error='Не удалось удалить. Попробуйте позже.')
    return '', 200


@mod_api.route('/repeat/add', methods=['POST'])
def add_repeat():
    if not request.json \
       or 'set_id' not in request.json \
       or 'weight' not in request.json \
       or 'count' not in request.json:
        abort(404)
    sets_instance = Sets.query.get(int(request.json['set_id']))
    if not sets_instance.user_id == current_user.id:
        return jsonify(error='Отказано в доступе')
    new_rep = Repeats(
        set_id=request.json['set_id'],
        weight=request.json['weight'],
        count=request.json['count']
    )
    db.session.add(new_rep)
    try:
        db.session.commit()
    except SQLAlchemyError:
        return jsonify(error='Не удалось сохранить. Попробуйте позже.')
    return '', 200


@mod_api.route('/repeat/edit', methods=['POST'])
def edit_repeat():
    if not request.json \
       or 'id' not in request.json \
       or 'weight' not in request.json \
       or 'count' not in request.json:
        abort(404)
    repeat_instance = Repeats.query.get(int(request.json['id']))
    sets_instance = Sets.query.get(repeat_instance.set_id)
    if not sets_instance.user_id == current_user.id:
        return jsonify(error='Отказано в доступе')
    repeat_instance.weight = request.json['weight']
    repeat_instance.count = request.json['count']
    try:
        db.session.commit()
    except SQLAlchemyError:
        return jsonify(error='Не удалось сохранить. Попробуйте позже.')
    return '', 200


@mod_api.route('/repeat/delete', methods=['POST'])
def delete_repeat():
    if not request.json \
       or 'id' not in request.json:
        abort(400)
    repeat_instance = Repeats.query.get(int(request.json['id']))
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
