from app import db
from flask import (
    Blueprint,
    jsonify,
    request
)
from flask_login import current_user, login_required
from .models import Programm
from app.mod_training.models import Exercises
from .forms import *
from werkzeug.datastructures import MultiDict
from sqlalchemy.exc import SQLAlchemyError

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
    form = ProgrammAdd(formdata=MultiDict({'name': data['name']}))
    if not form.validate():
        return jsonify(error='Проверьте введеные данные!')
    instance = Programm(
        name=form.name.data,
        user_id=current_user.id
    )
    db.session.add(instance)
    if not (data['exercises']):
        return jsonify(error='Не добавлено ни одного упражнения')
    for exercise in data['exercises']:
        exercise_form = IdForm(formdata=MultiDict({'id': exercise}))
        if not exercise_form.validate():
            return jsonify(error='Проверьте введеные данные!')
        # get exercise object then add to programms MtM
        exercise_instance = Exercises.query.get(exercise_form.id.data)
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
    form = ProgrammEdit(formdata=MultiDict(data))
    if not form.validate():
        return jsonify(error='Проверьте введеные данные!')
    instance = Programm.query.get(form.id.data)
    if instance is None:
        return jsonify(error="Object does not exist")
    if not instance.user_id == current_user.id:
        return jsonify(error='Отказано в доступе')
    instance.name = form.name.data
    try:
        db.session.commit()
    except SQLAlchemyError:
        return jsonify(error='Не удалось сохранить. Попробуйте позже.')
    return '', 200


@mod_programms.route('/add_exercise', methods=['POST'])
@login_required
def add_exercise_to_programm():
    data = request.get_json(force=True)
    form = AddExercise(formdata=MultiDict(data))
    if not form.validate():
        return jsonify(error='Проверьте введеные данные!')
    instance = Programm.query.get(form.id.data)
    if instance is None:
        return jsonify(error="Object does not exist")
    if not instance.user_id == current_user.id:
        return jsonify(error='Отказано в доступе')
    exercise = Exercises.query.get(form.new_exercise.data)
    if exercise is None:
        return jsonify(error="Object does not exist")
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
    form = ChangeExercise(formdata=MultiDict(data))
    if not form.validate():
        return jsonify(error='Проверьте введеные данные!')
    instance = Programm.query.get(form.id.data)
    if instance is None:
        return jsonify(error="Object does not exist")
    if not instance.user_id == current_user.id:
        return jsonify(error='Отказано в доступе')
    new_exercise = Exercises.query.get(form.new_exercise.data)
    old_exercise = Exercises.query.get(form.old_exercise.data)
    if new_exercise is None or old_exercise is None:
        return jsonify(error="Object does not exist")
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
    form = DeleteExercise(formdata=MultiDict(data))
    if not form.validate():
        return jsonify(error='Проверьте введеные данные!')
    programm_instance = Programm.query.get(form.id.data)
    if programm_instance is None:
        return jsonify(error="Object does not exist")
    if not programm_instance.user_id == current_user.id:
        return jsonify(error='Отказано в доступе')
    exercise_instance = Exercises.query.get(form.exercise_id.data)
    if exercise_instance is None:
        return jsonify(error="Object does not exist")
    programm_instance.exercise.remove(exercise_instance)
    try:
        db.session.commit()
    except SQLAlchemyError:
        return jsonify(error='Не удалось сохранить. Попробуйте позже.')
    return '', 200


@mod_programms.route('/delete', methods=['POST'])
@login_required
def delete_programm():
    data = request.get_json(force=True)
    form = IdForm(formdata=MultiDict(data))
    if not form.validate():
        return jsonify(error='Проверьте введеные данные!')
    instance = Programm.query.get(form.id.data)
    if instance is None:
        return jsonify(error="Object does not exist")
    if not instance.user_id == current_user.id:
        return jsonify(error='Отказано в доступе')
    try:
        db.session.delete(instance)
        db.session.commit()
    except SQLAlchemyError:
        return jsonify(error='Не удалось сохранить. Попробуйте позже.')
    return '', 200
