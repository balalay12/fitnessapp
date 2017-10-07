import calendar

from collections import defaultdict
from flask import (
    abort,
    Blueprint,
    jsonify,
    request
)
from flask_login import current_user, login_required
from .models import *
from .forms import (
    SetAdd,
    SetEdit,
    DeleteForm,
    RepsAdd,
    RepsAddWithId
)
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.datastructures import MultiDict

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
    dates = _get_dates(datetime.today().month, datetime.today().year)
    data = defaultdict(list)
    sets = [sets.serialize for sets in current_user.sets.filter(
        Sets.date >= dates['start'],
        Sets.date <= dates['end']
    ).all()]
    for item in sets:
        data[item['date']].append(item)
    return jsonify(sets=data)


@mod_training.route('/set_by_date/<month>/<year>', methods=['GET'])
@login_required
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


@mod_training.route('/set/add', methods=['POST'])
@login_required
def set_add():
    data = request.get_json(force=True)
    if 'training' not in data:
        abort(400)
    for training in data['training']:
        set_form = SetAdd(formdata=MultiDict({'date': training['date'], 'exercise': training['exercise']['id']}))
        if not set_form.validate():
            return jsonify(error='Проверьте введеные данные!')
        new_set = Sets(
            date=set_form.date.data,
            exercise_id=set_form.exercise.data,
            user_id=current_user.id
        )
        db.session.add(new_set)
        db.session.flush()
        for reps in training['sets']:
            rep_form = RepsAdd(formdata=MultiDict({'weight': reps['weight'], 'count': reps['count']}))
            if not rep_form.validate():
                return jsonify(error='Проверьте введеные данные!')
            new_reps = Repeats(
                set_id=new_set.id,
                weight=rep_form.weight.data,
                count=rep_form.count.data
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


@mod_training.route('/set/edit', methods=['POST'])
@login_required
def edit_set():
    data = request.get_json(force=True)
    form = SetEdit(formdata=MultiDict(data))
    if not form.validate():
        return jsonify(error='Проверьте введеные данные!')
    res = form.save()
    if 'error' in res:
        return jsonify(res)
    return '', 200


@mod_training.route('/set/delete', methods=['POST'])
@login_required
def delete_set():
    data = request.get_json(force=True)
    form = DeleteForm(formdata=MultiDict(data))
    if not form.validate():
        return jsonify(error='Проверьте введеные данные!')
    res = form.delete_set()
    if 'error' in res:
        return jsonify(res)
    return '', 200


@mod_training.route('/repeat/add', methods=['POST'])
@login_required
def add_repeat():
    data = request.get_json(force=True)
    form = RepsAddWithId(formdata=MultiDict(data))
    if not form.validate():
        return jsonify(error='Проверьте введеные данные!')
    res = form.save()
    if 'error' in res:
        return jsonify(res)
    return '', 200


@mod_training.route('/repeat/edit', methods=['POST'])
@login_required
def edit_repeat():
    data = request.get_json(force=True)
    form = RepsAddWithId(formdata=MultiDict(data))
    if not form.validate():
        return jsonify(error='Проверьте введеные данные!')
    res = form.update()
    if 'error' in res:
        return jsonify(res)
    return '', 200


@mod_training.route('/repeat/delete', methods=['POST'])
@login_required
def delete_repeat():
    data = request.get_json(force=True)
    form = DeleteForm(formdata=MultiDict(data))
    if not form.validate():
        return jsonify(error='Проверьте введеные данные!')
    res = form.delete_rep()
    if 'error' in res:
        return jsonify(res)
    return '', 200


def _get_dates(month, year):
    last_day = calendar.monthrange(int(year), int(month))[1]
    start = datetime(year=int(year), month=int(month), day=1)
    end = datetime(year=int(year), month=int(month), day=last_day)
    return {'start': start, 'end': end}
