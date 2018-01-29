import requests
import trafaret as t

from flask import (
    Blueprint, 
    request, 
    abort, 
    jsonify, 
    url_for, 
    redirect
)
from flask_login import login_user, logout_user, current_user, login_required
from app import bcrypt, db
from .models import User
from .validators import *
from sqlalchemy.exc import SQLAlchemyError

mod_auth = Blueprint('auth', __name__)

CLIENT_ID = '6141326'
CLIENT_SECRET = 'yh3WP7feYML3HzK9aOrQ'


@mod_auth.route('/login', methods=['POST'])
def login():
    # form = LoginForm(data=request.get_json(force=True))
    # if not form.validate():
    #     return jsonify(error='Проверьте введеные данные!')
    data = request.get_json(force=True)
    try:
        checking_data = login_validator.check(data)
    except t.DataError:
        return jsonify(error='Проверьте введеные данные!')
    try:
        user = User.query.filter_by(email=checking_data['email']).first()
    except SQLAlchemyError:
        return jsonify(error='Ошибка.')
    if user is None:
        return jsonify(error='Пользователь не найден.')
    if bcrypt.check_password_hash(user.password, checking_data['password']):
        login_user(user)
        return '', 200
    return jsonify(error='Не правильно введен пароль.')


@mod_auth.route('/registration', methods=['POST'])
def registration():
    # form = RegistrationForm(data=request.get_json(force=True))
    # if not form.validate():
    #     return jsonify(error='Проверьте введеные данные!')
    data = request.get_json(force=True)
    try:
        checking_data = registration_validator.check(data)
    except t.DataError:
        return jsonify(error='Проверьте введеные данные!')
    check_user_email = User.query.filter_by(email=checking_data['email']).first()
    if check_user_email is not None:
        return jsonify(error='Пользователь с такой почтой уже зарегестрирован')
    user = User(
        email=checking_data['email'],
        first_name=checking_data['first_name'],
        last_name=checking_data['last_name'],
        password=bcrypt.generate_password_hash(checking_data['password'])
    )
    try:
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify(error='Не удалось сохранить. Попробуйте позже.')
    return '', 200


@mod_auth.route('/vk_auth', methods=['GET'])
def vk_auth():

    url = "https://oauth.vk.com/authorize?" \
        "client_id={}&" \
        "scope=email&" \
        "response_type=code&" \
        "v=5.67&" \
        "redirect_uri=http://localhost:5000{}".format(CLIENT_ID, url_for(
            'auth.vk_response'))
    return redirect(url)


@mod_auth.route('/vk_response', methods=['GET'])
def vk_response():
    code = request.args.get('code')
    if code:
        url = "https://oauth.vk.com/access_token?" \
            "client_id={}&" \
            "client_secret={}&" \
            "code={}&" \
            "redirect_uri=http://localhost:5000{}".format(
                CLIENT_ID, 
                CLIENT_SECRET, 
                code, 
                url_for('auth.vk_response'))
        res = requests.get(url).json()
        # session['token'] = res['access_token']
        try:
            user = User.query.filter_by(vk_id=res['user_id']).first()
        except SQLAlchemyError as e:
            abort(500)
        if user is not None:
            login_user(user)
            return redirect('/')
        get_users_url = "https://api.vk.com/method/users.get?" \
                        "user_ids=%s&" \
                        "fields=photo_200&" \
                        "access_token=%s&v=5.67" % (res['user_id'], res['access_token'])
        users_get_raw = requests.get(get_users_url).json()
        users_get = users_get_raw['response'][0]
        user_email = ''
        if 'email' in res:
            user_email = res['email']
        user = User(
            email=user_email,
            first_name=users_get['first_name'],
            last_name=users_get['last_name'],
            vk_id=int(res['user_id'],),
            photo=users_get['photo_200']
        )
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            abort(500)
        login_user(user)
        return redirect('/')
    abort(500)


@mod_auth.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return jsonify(response='OK')


@mod_auth.route('/get_user', methods=['GET'])
@login_required
def get_user():
    # TODO: get user avatar from vk.com if user have vk_id in DB
    return jsonify(current_user.serialize)


@mod_auth.route('/goal', methods=['POST'])
@login_required
def user_goal():
    data = request.get_json(force=True)
    try:
        cheking_data = goal_validator.check(data)
    except t.DataError:
        return jsonify(error='Проверьте введеные данные!')
    try:
        User.query.filter_by(id=current_user.id).update({
            'goal': cheking_data['goal']
        })
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify(error='Не удалось сохранить. Попробуйте позже.')
    return '', 200


@mod_auth.route('/change_role_to_trainer', methods=['GET',])
@login_required
def change_role():
    if current_user.role == 'trainer':
        return jsonify(error='Вы уже являетесь тренером.')
    try:
        # TODO: create check role when table with roles live
        User.query.filter_by(id=current_user.id).update({
            'role': 'trainer'
        })
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify(error='Не удалось сохранить. Попробуйте позже.')
    return '', 200


@mod_auth.route('/trainer_info', methods=['POST',])
@login_required
def trainer_info():
    if not current_user.role == 'trainer':
        return jsonify(error='Вы не являетесь тренером.')
    data = request.get_json(force=True)
    try:
        checking_data = trainer_info_validator.check(data)
    except t.DataError:
        return jsonify(error='Проверьте введеные данные!')
    try:
        User.query.filter_by(id=current_user.id).update({
            'price': checking_data.get('price'),
            'description': checking_data.get('description')
        })
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify(error='Не удалось сохранить. Попробуйте позже.')
    return '', 200
