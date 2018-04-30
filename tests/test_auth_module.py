import json
import unittest
from app import db
from tests.testconf import BaseTestCase
from app.mod_auth.models import User


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

        # try registration with unvalid email
        response = self.client.post('/registration', data=json.dumps({
            'email': '@min.ru',
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

        # with empty params
        response = self.login(**{
            'email': '',
            'password': ''
        })
        self.assertEqual(response.json, dict(error='Проверьте введеные данные!'))

        # when user not in db
        response = self.login(**{
            'email': 'test1111@testmail.ru',
            'password': '111111111'
        })
        self.assertEqual(response.json, dict(error='Пользователь не найден.'))

        # ok
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

    def test_get_user(self):
        """TEST: get user"""

        # user not auth
        response = self.client.get('/get_user')
        self.assert401(response)

        # ok
        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })
        response = self.client.get('/get_user')
        self.assert200(response)

    def test_user_goal(self):
        """TEST: user goal"""

        data_empty = json.dumps({'goal': ''})
        data = json.dumps({'goal': 'user goal'})

        # user not auth
        response = self.client.post('/goal', data=data)
        self.assert401(response)

        # empty data
        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })
        response = self.client.post('/goal', data=data_empty)
        self.assert200(response)

        # not empty data
        response = self.client.post('/goal', data=data)
        self.assert200(response)

    def test_change_role(self):
        """TEST: change role"""

        # user not auth
        response = self.client.get('/change_role_to_trainer')
        self.assert401(response)

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        # ok
        response = self.client.get('/change_role_to_trainer')
        self.assert200(response)

        # when user is already trainer
        response = self.client.get('/change_role_to_trainer')
        self.assertEqual(response.json, dict(error='Вы уже являетесь тренером.'))

    def test_trainer_info(self):
        """TEST: trainer info"""

        data = json.dumps({
            'price': 500,
            'description': 'стаж 5000 лет'
        })
        empty_data = json.dumps({
            'price': '',
            'description': ''
        })
        one_field_data = json.dumps({
            'price': '100',
            'description': ''
        })

        # user not auth
        response = self.client.post('/trainer_info', data={})
        self.assert401(response)

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        # user is not trainer
        response = self.client.post('/trainer_info', data=data)
        self.assertEqual(response.json, dict(error='Вы не являетесь тренером.'))

        # set data
        self.client.get('/change_role_to_trainer')
        response = self.client.post('/trainer_info', data=data)
        self.assert200(response)

        response = self.client.get('/get_user')
        self.assertEqual(response.json['description'], 'стаж 5000 лет')
        self.assertEqual(response.json['price'], 500)

        # update data
        response = self.client.post('/trainer_info', data=one_field_data)
        self.assert200(response)

        response = self.client.get('/get_user')
        self.assertEqual(response.json['description'], '')
        self.assertEqual(response.json['price'], 100)

    def test_get_clients(self):
        """TEST: get clients"""

        response = self.client.get('/get_clients')
        self.assert401(response)

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })
        response = self.client.get('/get_clients')
        self.assertEqual(response.json, dict(error='Вы не являетесь тренером.'))

        # add client into DB
        client = User(
            email='cli@ent.ru',
            password='client',
            first_name='Client',
            last_name='Clientovich',
            trainer_id=1
        )
        db.session.add(client)
        db.session.commit()

        self.client.get('/change_role_to_trainer')
        response = self.client.get('/get_clients')
        self.assert200(response)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(
            response.json['clients'][0]['first_name'],
            'Client'
        )


if __name__ == '__main__':
    unittest.main()