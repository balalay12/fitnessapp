from app import db
from flask import (
    Blueprint,
    request,
    jsonify,
)
from flask_login import current_user, login_required
from .validators import *
from .models import Anthropometry
from sqlalchemy.exc import SQLAlchemyError
from app.mod_auth.models import User

mod_anthropometry = Blueprint('anthropometry', __name__, url_prefix='/anthropometry')


@mod_anthropometry.route('/', methods=['GET'])
@login_required
def read():
    client_id = request.args.get('id')
    if client_id:
        client = User.query.get(int(client_id))
        if client is None:
            return jsonify(error='Клиент не найден')
        if not client.trainer_id == current_user.id:
            return jsonify(error='Отказано в доступе')
        anthropometry = client.anthropometry.all()
    else:
        anthropometry = current_user.anthropometry.all()
    return jsonify(anthropometry=[item.serialize for item in anthropometry])


@mod_anthropometry.route('/add', methods=['POST'])
@login_required
def add():
    data = request.get_json(force=True)
    try:
        checking_data = add_body_size_validator.check(data)
    except t.DataError:
        return jsonify(error='Проверьте введеные данные!')

    new_anthropometry = Anthropometry(
        neck=checking_data.get('neck'),
        chest=checking_data.get('chest'),
        waist=checking_data.get('waist'),
        forearm=checking_data.get('forearm'),
        arm=checking_data.get('arm'),
        hip=checking_data.get('hip'),
        shin=checking_data.get('shin'),
        user_id=current_user.id
    )
    db.session.add(new_anthropometry)
    try:
        db.session.commit()
    except SQLAlchemyError:
        return jsonify(error='Не удалось сохранить. Попробуйте позже.')
    return '', 200


@mod_anthropometry.route('/edit', methods=['POST'])
@login_required
def edit():
    data = request.get_json(force=True)
    try:
        checking_data = edit_body_size_validator.check(data)
    except t.DataError:
        return jsonify(error='Проверьте введеные данные!')

    instance = Anthropometry.query.get(checking_data.get('id'))
    if instance is None:
        return jsonify(error='Объект не найден')
    if not instance.user_id == current_user.id:
        return jsonify(error='Отказано в доступе')
    instance.neck = checking_data.get('neck')
    instance.chest = checking_data.get('chest')
    instance.waist = checking_data.get('waist')
    instance.forearm = checking_data.get('forearm')
    instance.arm = checking_data.get('arm')
    instance.hip = checking_data.get('hip')
    instance.shin = checking_data.get('shin')
    try:
        db.session.commit()
    except SQLAlchemyError:
        return jsonify(error='Не удалось сохранить. Попробуйте позже.')
    return '', 200


@mod_anthropometry.route('/delete/<id>', methods=['GET'])
@login_required
def remove(id):
    try:
        id = int(id)
    except ValueError:
        return jsonify(error='Ошибка.')
    instance = Anthropometry.query.get(id)
    if instance is None:
        return jsonify(error='Объект не найден')
    if not instance.user_id == current_user.id:
        return jsonify(error='Отказано в доступе')
    try:
        db.session.delete(instance)
        db.session.commit()
    except SQLAlchemyError:
        return jsonify(error='Не удалось сохранить. Попробуйте позже.')
    return '', 200
