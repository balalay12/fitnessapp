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
        abort(500)
    return '', 200


def _get_dates(month, year):
    last_day = calendar.monthrange(int(year), int(month))[1]
    start = datetime(year=int(year), month=int(month), day=1)
    end = datetime(year=int(year), month=int(month), day=last_day)
    return {'start': start, 'end': end}
