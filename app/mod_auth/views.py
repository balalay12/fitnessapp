import requests

from flask import (
    Blueprint, 
    request, 
    abort, 
    jsonify, 
    url_for, 
    redirect,
    session
)
from flask_login import login_user, logout_user
from app import bcrypt, db
from .models import User
from sqlalchemy.exc import SQLAlchemyError

mod_auth = Blueprint('auth', __name__)

CLIENT_ID = '6141326'
CLIENT_SECRET = 'yh3WP7feYML3HzK9aOrQ'

@mod_auth.route('/login', methods=['POST'])
def login():
    if not request.json \
        or not 'email' in request.json \
        or not 'password' in request.json:
        abort(400)
    try:
        user = User.query.filter_by(username=request.json['email']).first()
    except SQLAlchemyError as e:
        abort(500)
    if user is None:
        abort(404)
    if bcrypt.check_password_hash(user.password, request.json['password']):
        login_user(user)
        print('user is loged')
        return '', 200
    return 'jsonify()'


@mod_auth.route('/registration', methods=['POST'])
def registration():
    if not request.json \
        or not 'first_name' in request.json \
        or not 'last_name' in request.json \
        or not 'email' in request.json \
        or not 'password' in request.json:
        abort(400)
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
        abort(500)
    return 'jsonify()'


@mod_auth.route('/vk_auth', methods=['GET'])
def vk_auth():

    url = "https://oauth.vk.com/authorize?" \
        "client_id={}&" \
        "scope=email&" \
        "response_type=code&" \
        "v=5.67&" \
        "redirect_uri=http://localhost:5000{}".format(CLIENT_ID, url_for(
            'auth.vk_responce'))
    return redirect(url)


@mod_auth.route('/vk_response', methods=['GET'])
def vk_responce():
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
                url_for('auth.vk_responce'))
        res = requests.get(url).json()
        session['token'] = res['access_token']
        try:
            user = User.query.filter_by(email=res['email'], vk_id=res['user_id']).first()
        except SQLAlchemyError as e:
            abort(500)
        if user is not None:
            login_user(user)
            return 'login', 200
        user = User(
            email=res['email'],
            vk_id=int(res['user_id'])
        )
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500)
        login_user(user)
        return redirect('/')
    abort(500)



@mod_auth.route('/logout', methods=['GET'])
def logout():
    print('user log out')
    logout_user()
    return '', 200
