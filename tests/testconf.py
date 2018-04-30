import json
import unittest

from app import app, db, bcrypt
from app.mod_training.models import *
from app.mod_auth.models import User
from flask_testing import TestCase


class BaseTestCase(TestCase):

    # data for tests
    set200 = {'training': [
        {
            'date': '2017-9-27',
            'exercise': 1,
            'sets': [
                {'weight': 60, 'count': 12},
                {'weight': 60, 'count': 12}
            ]
        },
        {
            'date': '2017-9-20',
            'exercise': 2,
            'sets': [
                {'weight': 60, 'count': 12},
                {'weight': 60, 'count': 12}
            ]
        }
    ]}

    bad_exercise_set = {'training': [
        {
            'date': '2017-9-27',
            'exercise': '',
            'sets': [
                {'weight': 'xdvfvzvzcxv', 'count': 'asdfasdfadsf'},
                {'weight': '', 'count': 12}
            ]
        }
    ]}

    bad_repeat_set = {'training': [
        {
            'date': '2017-9-27',
            'exercise': 1,
            'sets': [
                {'weight': '', 'count': 'asdfasdfadsf'},
                {'weight': '', 'count': 12}
            ]
        }
    ]}

    edit_set_200 = {
        'id': 1,
        'exercise_id': 2
    }

    edit_set_400 = {
        'id': 'asdf',
        'exercise_id': ''
    }

    edit_set_not_exist = {
        'id': 99,
        'exercise_id': 2
    }

    delete_200 = {
        'id': 1
    }

    delete_json = {
        'id': 'ads'
    }

    delete_set_not_exist = {
        'id': 99
    }

    repeat_add_200 = {
        'id': 1,
        'weight': 20,
        'count': 30
    }

    repeat_add_set_not_exist = {
        'id': 99,
        'weight': 20,
        'count': 30
    }

    repeat_add_json_error = {
        'id': '',
        'weight': 20,
        'count': 30
    }

    repeat_edit_200 = {
        'id': 1,
        'weight': 20,
        'count': 30
    }

    repeat_edit_not_exist = {
        'id': 99,
        'weight': 20,
        'count': 30
    }

    repeat_edit_json_error = {
        'id': '',
        'weight': 20,
        'count': 30
    }

    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()
        user = User(
            email='ad@min.ru',
            password=bcrypt.generate_password_hash('adminadmin'),
            first_name='Ivan',
            last_name='Ivanov'
        )
        user2 =  User(
            email='us@er.ru',
            password=bcrypt.generate_password_hash('useruser'),
            first_name='User',
            last_name='Userovich'
        )
        legs = Categories(
            name='Ноги'
        )
        back = Categories(
            name='Спина'
        )
        ex1 = Exercises(
            name='Приседания',
            category_id=1
        )
        ex2 = Exercises(
            name='Становая',
            category_id=2
        )
        ex3 = Exercises(
            name='Test',
            category_id=2
        )
        db.session.add(user)
        db.session.add(user2)
        db.session.add(legs)
        db.session.add(back)
        db.session.add(ex1)
        db.session.add(ex2)
        db.session.add(ex3)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, email, password):
        data = dict(
            email=email,
            password=password
        )
        return self.client.post('/login', data=json.dumps(data))

    def logout(self):
        return self.client.get('/logout')
