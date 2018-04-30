import json
from tests.testconf import BaseTestCase


class AnthropometryTest(BaseTestCase):
    """TEST: anthropometry test"""

    anthropometry_200 = {
        'neck': 70.0
    }

    anthropometry_edit = {
        'id': 1,
        'chest': 70.0,
    }

    anthropometry_object_does_not_exist = {
        'id': 99,
        'chest': 70.0,
    }

    anthropometry_error = {
        'neck': 'adsf',
    }

    def test_anthropometry_read(self):
        response = self.client.get('/anthropometry/')
        self.assert401(response)

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        response = self.client.post('/anthropometry/add', data=json.dumps(self.anthropometry_200))
        self.assert200(response)

        response = self.client.get('/anthropometry/')
        self.assertEqual(len(response.json['anthropometry']), 1)

    def test_anthropometry_add(self):
        response = self.client.post('/anthropometry/add', data=json.dumps(self.anthropometry_200))
        self.assert401(response)

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        response = self.client.post('/anthropometry/add', data=json.dumps(self.anthropometry_error))
        self.assertEqual(response.json, dict(error='Проверьте введеные данные!'))

        response = self.client.post('/anthropometry/add', data=json.dumps(self.anthropometry_200))
        self.assert200(response)

    def test_anthropometry_edit(self):
        response = self.client.post(
            '/anthropometry/edit',
            data=json.dumps(self.anthropometry_200))
        self.assert401(response)

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        response = self.client.post(
            '/anthropometry/add',
            data=json.dumps(self.anthropometry_200))
        self.assert200(response)

        response = self.client.post(
            '/anthropometry/edit',
            data=json.dumps(self.anthropometry_object_does_not_exist))
        self.assertEqual(response.json, dict(error='Объект не найден'))

        response = self.client.post(
            '/anthropometry/edit',
            data=json.dumps(self.anthropometry_edit))
        self.assert200(response)

        response = self.client.get('/logout')
        self.assertEqual(response.json, dict(response='OK'))

        self.login(**{
            'email': 'us@er.ru',
            'password': 'useruser'
        })

        response = self.client.post('/anthropometry/edit', data=json.dumps(self.anthropometry_edit))
        self.assertEqual(response.json, dict(error='Отказано в доступе'))

    def test_anthropometry_remove(self):
        response = self.client.get('/anthropometry/delete/1')
        self.assert401(response)

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        response = self.client.get('/anthropometry/delete/asdfasdfasdf')
        self.assertEqual(response.json, dict(error='Ошибка.'))

        response = self.client.get('/anthropometry/delete/1')
        self.assertEqual(response.json, dict(error='Объект не найден'))

        response = self.client.post(
            '/anthropometry/add',
            data=json.dumps(self.anthropometry_200))
        self.assert200(response)

        response = self.client.get('/logout')
        self.assertEqual(response.json, dict(response='OK'))

        self.login(**{
            'email': 'us@er.ru',
            'password': 'useruser'
        })

        response = self.client.get('/anthropometry/delete/1')
        self.assertEqual(response.json, dict(error='Отказано в доступе'))

        response = self.client.get('/logout')
        self.assertEqual(response.json, dict(response='OK'))

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        response = self.client.get('/anthropometry/delete/1')
        self.assert200(response)
