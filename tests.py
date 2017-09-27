import json
import unittest

from app import app, db, bcrypt
from app.mod_api.models import *
from app.mod_auth.models import User
from flask_testing import TestCase


class BaseTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
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
        db.session.add(user)
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


if __name__ == '__main__':
    unittest.main()
