from app import db
from flask import (
    Blueprint,
    request,
    jsonify
)
from flask_login import current_user, login_required
from .forms import BodySizeAdd, BodySizeEdit
from .models import Anthropometry
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.datastructures import MultiDict

mod_anthropometry = Blueprint('anthropometry', __name__, url_prefix='/anthropometry')


@mod_anthropometry.route('/', methods=['GET'])
@login_required
def read():
    anthropometry = current_user.anthropometry.all()
    return jsonify(anthropometry=[item.serialize for item in anthropometry])


@mod_anthropometry.route('/add', methods=['POST'])
@login_required
def add():
    data = request.get_json(force=True)
    form = BodySizeAdd(formdata=MultiDict(data))
    if not form.validate():
        return jsonify(error='Проверьте введеные данные!')
    new_anthropometry = Anthropometry(
        neck=form.neck.data,
        chest=form.chest.data,
        waist=form.waist.data,
        forearm=form.forearm.data,
        arm=form.arm.data,
        hip=form.hip.data,
        shin=form.shin.data,
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
    form = BodySizeEdit(formdata=MultiDict(data))
    if not form.validate():
        return jsonify(error='Проверьте введеные данные!')
    instance = Anthropometry.query.get(form.id.data)
    if instance is None:
        return jsonify(error='Объект не найден')
    if not instance.user_id == current_user.id:
        return jsonify(error='Отказано в доступе')
    instance.neck = form.neck.data
    instance.chest = form.chest.data
    instance.waist = form.waist.data
    instance.forearm = form.forearm.data
    instance.arm = form.arm.data
    instance.hip = form.hip.data
    instance.shin = form.shin.data
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
