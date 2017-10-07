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

from app.base_api_view import BaseApiView

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
    res = form.save()
    if 'error' in res:
        return jsonify(res)
    return '', 200


@mod_anthropometry.route('/edit', methods=['POST'])
@login_required
def edit():
    data = request.get_json(force=True)
    form = BodySizeEdit(formdata=MultiDict(data))
    if not form.validate():
        return jsonify(error='Проверьте введеные данные!')
    res = form.save()
    if 'error' in res:
        return jsonify(res)
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
        return jsonify(error='Ошибка.')
    if not instance.user_id == current_user.id:
        return jsonify(error='Отказано в доступе')
    try:
        db.session.delete(instance)
        db.session.commit()
    except SQLAlchemyError:
        return jsonify(error='Не удалось сохранить. Попробуйте позже.')
    return '', 200
