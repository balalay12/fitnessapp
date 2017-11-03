from app import db
from flask import (
    Blueprint,
    jsonify,
    request
)
from flask_login import current_user, login_required
from .models import Programm
from app.mod_training.models import Exercises
from .validators import *
from sqlalchemy.exc import SQLAlchemyError
import trafaret as t

mod_programms = Blueprint('programms', __name__, url_prefix='/programms')


@mod_programms.route('/', methods=['GET'])
@login_required
def read():
    programms_query = Programm.query.filter_by(user_id=current_user.id)
    programms = []
    for programm in programms_query:
        exercises = []
        out = programm.serialize.copy()
        for ex in programm.exercise:
            exercises.append(ex.serialize)
        out['exercises'] = exercises
        programms.append(out)
    return jsonify(programms=programms)


@mod_programms.route('/add', methods=['POST'])
@login_required
def add():
    data = request.get_json(force=True)
    try:
        checking_data = add_programm.check(data)
    except t.DataError:
        return jsonify(error='Проверьте введеные данные!')
    instance = Programm(
        name=checking_data.get('name'),
        user_id=current_user.id
    )
    db.session.add(instance)
    if not (checking_data.get('exercises')):
        return jsonify(error='Не добавлено ни одного упражнения')
    for exercise in checking_data.get('exercises'):
        # get exercise object then add to programms MtM
        exercise_instance = Exercises.query.get(exercise)
        if exercise_instance is None:
            return jsonify(error='Упраженния с таким ID не найдено')
        instance.exercise.append(exercise_instance)
    try:
        db.session.commit()
    except SQLAlchemyError:
        return jsonify(error='Не удалось сохранить. Попробуйте позже.')
    return '', 200


@mod_programms.route('/edit', methods=['POST'])
@login_required
def update_programm_name():
    data = request.get_json(force=True)
    try:
        checking_data = edit_programm_name.check(data)
    except t.DataError:
        return jsonify(error='Проверьте введеные данные!')
    instance = Programm.query.get(checking_data.get('id'))
    if instance is None:
        return jsonify(error='Программы с таким ID не найдено')
    if not instance.user_id == current_user.id:
        return jsonify(error='Отказано в доступе')
    instance.name = checking_data.get('name')
    try:
        db.session.commit()
    except SQLAlchemyError:
        return jsonify(error='Не удалось сохранить. Попробуйте позже.')
    return '', 200


@mod_programms.route('/add_exercise', methods=['POST'])
@login_required
def add_exercise_to_programm():
    data = request.get_json(force=True)
    try:
        checking_data = add_exercise.check(data)
    except t.DataError:
        return jsonify(error='Проверьте введеные данные!')
    instance = Programm.query.get(checking_data.get('id'))
    if instance is None:
        return jsonify(error='Программы с таким ID не найдено')
    if not instance.user_id == current_user.id:
        return jsonify(error='Отказано в доступе')
    exercise = Exercises.query.get(checking_data.get('new_exercise'))
    if exercise is None:
        return jsonify(error='Упражнения с таким ID не найдено')
    instance.exercise.append(exercise)
    try:
        db.session.commit()
    except SQLAlchemyError:
        return jsonify(error='Не удалось сохранить. Попробуйте позже.')
    return '', 200


@mod_programms.route('/edit_exercise', methods=['POST'])
@login_required
def change_exercise_in_programm():
    data = request.get_json(force=True)
    try:
        checking_data = change_exercise.check(data)
    except t.DataError:
        return jsonify(error='Проверьте введеные данные!')
    instance = Programm.query.get(checking_data.get('id'))
    if instance is None:
        return jsonify(error='Программы с таким ID не найдено')
    if not instance.user_id == current_user.id:
        return jsonify(error='Отказано в доступе')
    new_exercise = Exercises.query.get(checking_data.get('new_exercise'))
    old_exercise = Exercises.query.get(checking_data.get('old_exercise'))
    if new_exercise is None or old_exercise is None:
        return jsonify(error='Упражнения с таким ID не найдено')
    # delete old exercise from programm
    instance.exercise.remove(old_exercise)
    # add new exercise to programm
    instance.exercise.append(new_exercise)
    try:
        db.session.commit()
    except SQLAlchemyError:
        return jsonify(error='Не удалось сохранить. Попробуйте позже.')
    return '', 200


@mod_programms.route('/delete_exercise', methods=['POST'])
@login_required
def delete_exercise_from_programm():
    data = request.get_json(force=True)
    try:
        checking_data = delete_exercise.check(data)
    except t.DataError:
        return jsonify(error='Проверьте введеные данные!')
    programm_instance = Programm.query.get(checking_data.get('id'))
    if programm_instance is None:
        return jsonify(error='Программы с таким ID не найдено')
    if not programm_instance.user_id == current_user.id:
        return jsonify(error='Отказано в доступе')
    exercise_instance = Exercises.query.get(checking_data.get('exercise_id'))
    if exercise_instance is None:
        return jsonify(error='Упражнения с таким ID не найдено')
    programm_instance.exercise.remove(exercise_instance)
    try:
        db.session.commit()
    except SQLAlchemyError:
        return jsonify(error='Не удалось сохранить. Попробуйте позже.')
    return '', 200


@mod_programms.route('/delete/<id>', methods=['DELETE'])
@login_required
def delete_programm(id):
    try:
        programm_id = t.Int().check(id)
    except t.DataError:
        return jsonify(error='Проверьте введеные данные!')
    instance = Programm.query.get(programm_id)
    if instance is None:
        return jsonify(error='Программы с таким ID не найдено')
    if not instance.user_id == current_user.id:
        return jsonify(error='Отказано в доступе')
    try:
        db.session.delete(instance)
        db.session.commit()
    except SQLAlchemyError:
        return jsonify(error='Не удалось сохранить. Попробуйте позже.')
    return '', 200
