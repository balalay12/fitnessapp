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
        weight=form.weight.data,
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
    print(data)
    form = BodySizeEdit(formdata=MultiDict(data))
    if not form.validate():
        return jsonify(error='Проверьте введеные данные!')
    anthropometry_instance = Anthropometry.query.get(form.id.data)
    if not anthropometry_instance.user_id == current_user.id:
        return jsonify(error='Отказано в доступе')
    anthropometry_instance.weight = form.weight.data
    anthropometry_instance.neck = form.neck.data
    anthropometry_instance.chest = form.chest.data
    anthropometry_instance.waist = form.waist.data
    anthropometry_instance.forearm = form.forearm.data
    anthropometry_instance.arm = form.arm.data
    anthropometry_instance.hip = form.hip.data
    anthropometry_instance.shin = form.shin.data
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
    anthropometry_instance = Anthropometry.query.get(id)
    if anthropometry_instance is None:
        return jsonify(error='Ошибка.')
    if not anthropometry_instance.user_id == current_user.id:
        return jsonify(error='Отказано в доступе')
    try:
        db.session.delete(anthropometry_instance)
        db.session.commit()
    except SQLAlchemyError:
        return jsonify(error='Не удалось сохранить. Попробуйте позже.')
    return '', 200
