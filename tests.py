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
            'exercise': {
                'id': 1
            },
            'sets': [
                {'weight': 60, 'count': 12},
                {'weight': 60, 'count': 12}
            ]
        },
        {
            'date': '2017-9-20',
            'exercise': {
                'id': 1
            },
            'sets': [
                {'weight': 60, 'count': 12},
                {'weight': 60, 'count': 12}
            ]
        }
    ]}

    bad_exercise_set = {'training': [
        {
            'date': '2017-9-27',
            'exercise': {
                'id': ''
            },
            'sets': [
                {'weight': 'xdvfvzvzcxv', 'count': 'asdfasdfadsf'},
                {'weight': '', 'count': 12}
            ]
        }
    ]}

    bad_repeat_set = {'training': [
        {
            'date': '2017-9-27',
            'exercise': {
                'id': 1
            },
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

    delete_200 = {
        'id': 1
    }

    delete_json = {
        'id': 'ads'
    }

    delete_404 = {
        'blah': ''
    }

    repeat_add_200 = {
        'id': 1,
        'weight': 20,
        'count': 30
    }

    repeat_add_400 = {

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

    repeat_edit_400 = {
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
        db.session.add(user)
        db.session.add(user2)
        db.session.add(legs)
        db.session.add(back)
        db.session.add(ex1)
        db.session.add(ex2)
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


class AuthTest(BaseTestCase):

    def test_registration(self):
        """TEST: user registration"""

        # try registration with empty fields
        response = self.client.post('/registration', data=json.dumps({
            'email': 'rwas@test.ru',
            'password': '1111111111',
            'first_name': '',
            'last_name': ''
        }))
        self.assertEqual(response.json, dict(error='Проверьте введеные данные!'))

        # try registration with
        response = self.client.post('/registration', data=json.dumps({
            'email': 'ad@min.ru',
            'password': '1111111111',
            'first_name': '',
            'last_name': ''
        }))
        self.assertEqual(response.json, dict(error='Проверьте введеные данные!'))

        # try registration with good data
        response = self.client.post('/registration', data=json.dumps({
            'email': 'test@test.ru',
            'password': 'testtest',
            'first_name': 'test',
            'last_name': 'test'
        }))
        self.assert200(response)

    def test_login(self):
        """TEST: user login"""

        response = self.login(**{
            'email': '',
            'password': ''
        })
        self.assertEqual(response.json, dict(error='Проверьте введеные данные!'))

        response = self.login(**{
            'email': 'test1111@testmail.ru',
            'password': '111111111'
        })
        self.assertEqual(response.json, dict(error='Пользователь не найден.'))

        response = self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })
        self.assert200(response)

    def test_logout(self):
        """TEST: user logout"""

        response = self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })
        self.assert200(response)

        response = self.client.get('/logout')
        self.assertEqual(response.json, dict(response='OK'))


class TrainingTest(BaseTestCase):
    """ TEST: training tests"""

    def test_categories(self):
        response = self.client.get('/training/categories')
        self.assertEqual(len(response.json['categories']), 2)

    def test_exercises(self):
        response = self.client.get('/training/exercises')
        self.assertEqual(len(response.json['exercises']), 2)

    def test_get_sets(self):
        response = self.client.get('/training/sets')
        self.assert401(response)

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })
        response = self.client.get('/training/sets')
        self.assert200(response)

    def test_get_sets_by_date(self):
        response = self.client.get('/training/set_by_date/9/2017')
        self.assert401(response)

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })
        response = self.client.get('/training/sets')
        self.assert200(response)

    def test_add_set(self):
        empty = {}

        response = self.client.post('/training/set/add', data=json.dumps(self.set200))
        self.assert401(response)

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        response = self.client.post('/training/set/add', data=json.dumps(empty))
        self.assert400(response)

        response = self.client.post('/training/set/add', data=json.dumps(self.bad_exercise_set))
        self.assertEqual(response.json, dict(error='Проверьте введеные данные!'))

        response = self.client.post('/training/set/add', data=json.dumps(self.bad_repeat_set))
        self.assertEqual(response.json, dict(error='Проверьте введеные данные!'))

        response = self.client.post('/training/set/add', data=json.dumps(self.set200))
        self.assert200(response)

        response = self.client.get('/training/sets')
        self.assert200(response)

    def test_set_edit(self):
        response = self.client.post('/training/set/edit', data=json.dumps({}))
        self.assert401(response)

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        response = self.client.post('/training/set/add', data=json.dumps(self.set200))
        self.assert200(response)

        response = self.client.post('/training/set/edit', data=json.dumps(self.edit_set_400))
        self.assertEqual(response.json, dict(error='Проверьте введеные данные!'))

        response = self.client.post('/training/set/edit', data=json.dumps(self.edit_set_200))
        self.assert200(response)

        response = self.client.get('/logout')
        self.assertEqual(response.json, dict(response='OK'))

        self.login(**{
            'email': 'us@er.ru',
            'password': 'useruser'
        })

        response = self.client.post('/training/set/edit', data=json.dumps(self.edit_set_200))
        self.assertEqual(response.json, dict(error='Отказано в доступе'))

    def test_set_delete(self):
        response = self.client.post('/training/set/delete', data=json.dumps({}))
        self.assert401(response)

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        response = self.client.post('/training/set/add', data=json.dumps(self.set200))
        self.assert200(response)

        response = self.client.get('/logout')
        self.assertEqual(response.json, dict(response='OK'))

        self.login(**{
            'email': 'us@er.ru',
            'password': 'useruser'
        })

        response = self.client.post('/training/set/delete', data=json.dumps(self.delete_200))
        self.assertEqual(response.json, dict(error='Отказано в доступе'))

        response = self.client.get('/logout')
        self.assertEqual(response.json, dict(response='OK'))

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        response = self.client.post('/training/set/delete', data=json.dumps(self.delete_json))
        self.assertEqual(response.json, dict(error='Проверьте введеные данные!'))

        response = self.client.post('/training/set/delete', data=json.dumps(self.delete_200))
        self.assert200(response)

    def test_repeat_add(self):
        response = self.client.post('/training/repeat/add', data=json.dumps({}))
        self.assert401(response)

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        response = self.client.post('/training/set/add', data=json.dumps(self.set200))
        self.assert200(response)

        response = self.client.post('/training/repeat/add', data=json.dumps(self.repeat_add_json_error))
        self.assertEqual(response.json, dict(error='Проверьте введеные данные!'))

        response = self.client.post('/training/repeat/add', data=json.dumps(self.repeat_add_200))
        self.assert200(response)

    def test_repeat_edit(self):
        response = self.client.post('/training/repeat/edit', data=json.dumps({}))
        self.assert401(response)

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        # response = self.client.post('/training/repeat/edit', data=json.dumps(self.repeat_edit_400))
        # self.assert404(response)

        response = self.client.post('/training/repeat/edit', data=json.dumps(self.repeat_edit_json_error))
        self.assertEqual(response.json, dict(error='Проверьте введеные данные!'))

        response = self.client.post('/training/set/add', data=json.dumps(self.set200))
        self.assert200(response)

        response = self.client.post('/training/repeat/edit', data=json.dumps(self.repeat_edit_200))
        self.assert200(response)

        response = self.client.get('/logout')
        self.assertEqual(response.json, dict(response='OK'))

        self.login(**{
            'email': 'us@er.ru',
            'password': 'useruser'
        })

        response = self.client.post('/training/repeat/edit', data=json.dumps(self.repeat_edit_200))
        self.assertEqual(response.json, dict(error='Отказано в доступе'))

    def test_repeat_delete(self):
        response = self.client.post('/training/repeat/delete', data=json.dumps({}))
        self.assert401(response)

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        response = self.client.post('/training/repeat/delete', data=json.dumps(self.delete_json))
        self.assertEqual(response.json, dict(error='Проверьте введеные данные!'))

        response = self.client.post('/training/set/add', data=json.dumps(self.set200))
        self.assert200(response)

        response = self.client.get('/logout')
        self.assertEqual(response.json, dict(response='OK'))

        self.login(**{
            'email': 'us@er.ru',
            'password': 'useruser'
        })

        response = self.client.post('/training/repeat/delete', data=json.dumps(self.delete_200))
        self.assertEqual(response.json, dict(error='Отказано в доступе'))

        response = self.client.get('/logout')
        self.assertEqual(response.json, dict(response='OK'))

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        response = self.client.post('/training/repeat/delete', data=json.dumps(self.delete_200))
        self.assert200(response)


if __name__ == '__main__':
    unittest.main()