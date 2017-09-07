import requests

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
from sqlalchemy.exc import SQLAlchemyError

mod_auth = Blueprint('auth', __name__)

CLIENT_ID = '6141326'
CLIENT_SECRET = 'yh3WP7feYML3HzK9aOrQ'


@mod_auth.route('/login', methods=['POST'])
def login():
    if not request.json \
       or 'email' not in request.json \
       or 'password' not in request.json:
        abort(400)
    try:
        user = User.query.filter_by(email=request.json['email']).first()
    except SQLAlchemyError as e:
        abort(500)
    if user is None:
        return jsonify(error='Пользователь не найден.')
    if bcrypt.check_password_hash(user.password, request.json['password']):
        login_user(user)
        return '', 200
    return jsonify(error='Не правильно введен пароль.')


@mod_auth.route('/registration', methods=['POST'])
def registration():
    if not request.json \
       or 'first_name' not in request.json \
       or 'last_name' not in request.json \
       or 'email' not in request.json \
       or 'password' not in request.json:
        abort(400)
    check_user_email = User.query.filter_by(email=request.json['email']).first()
    if check_user_email is not None:
        return jsonify(error='Пользователь с такой почтой уже зарегестрирован')
    user = User(
        email=request.json['email'],
        first_name=request.json['first_name'],
        last_name=request.json['last_name'],
        password=bcrypt.generate_password_hash(request.json['password'])
    )
    try:
        db.session.add(user)
        db.session.commit()
        return '', 200
    except SQLAlchemyError as e:
        db.session.rollback()
        # return jsonify(error=e)
        abort(500)


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
        get_users_url = f"https://api.vk.com/method/users.get?user_ids={res['user_id']}&fields=photo_200&access_token={res['access_token']}&v=5.67"
        users_get_raw = requests.get(get_users_url).json()
        users_get = users_get_raw['response'][0]
        user = User(
            # email=res['email'],
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
    return jsonify(first_name=current_user.first_name,
                   last_name=current_user.last_name,
                   photo=current_user.photo,)
