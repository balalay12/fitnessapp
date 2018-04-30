import json
from tests.testconf import BaseTestCase


class TrainingTest(BaseTestCase):
    """ TEST: training tests"""

    # programm data set
    programm_add_200 = {
        'name': 'Test',
        'exercises': [1, 3]
    }

    # data set for planning training
    plannig_200 = {
        'programm_id': 1,
        'date': '2017-10-22',
    }

    plannig_not_exitst = {
        'programm_id': 99,
        'date': '2017-10-22',
    }

    def test_categories(self):
        response = self.client.get('/training/categories')
        self.assertEqual(len(response.json['categories']), 2)

    def test_exercises(self):
        response = self.client.get('/training/exercises')
        self.assertEqual(len(response.json['exercises']), 3)

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

        response = self.client.post(
            '/training/set/add',
            data=json.dumps(self.bad_exercise_set)
        )
        self.assertEqual(response.json, dict(error='Проверьте введеные данные!'))

        response = self.client.post(
            '/training/set/add',
            data=json.dumps(self.bad_repeat_set)
        )
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

        response = self.client.post(
            '/training/set/edit',
            data=json.dumps(self.edit_set_400)
        )
        self.assertEqual(response.json, dict(error='Проверьте введеные данные!'))

        response = self.client.post(
            '/training/set/edit',
            data=json.dumps(self.edit_set_not_exist)
        )
        self.assertEqual(response.json, dict(error='Подхода с таким ID не найдено'))

        response = self.client.post(
            '/training/set/edit',
            data=json.dumps(self.edit_set_200)
        )
        self.assert200(response)

        response = self.client.get('/logout')
        self.assertEqual(response.json, dict(response='OK'))

        self.login(**{
            'email': 'us@er.ru',
            'password': 'useruser'
        })

        response = self.client.post(
            '/training/set/edit',
            data=json.dumps(self.edit_set_200)
        )
        self.assertEqual(response.json, dict(error='Отказано в доступе'))

    def test_planning_set(self):
        response = self.client.post(
            '/training/planning', data=json.dumps(self.plannig_200)
        )
        self.assert401(response)

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        response = self.client.post(
            '/programms/add', data=json.dumps(self.programm_add_200)
        )
        self.assert200(response)

        response = self.client.post(
            '/training/planning', data=json.dumps(self.plannig_not_exitst)
        )
        self.assertEqual(response.json, dict(error='Программы с таким ID не найдено'))

        response = self.client.post(
            '/training/planning', data=json.dumps(self.plannig_200)
        )
        self.assertEqual(response.json, dict(response='ok'))

        response = self.client.get('/training/set_by_date/10/2017')
        self.assertEqual(len(response.json['sets']['2017-10-22']), 2)

    def test_set_delete(self):
        response = self.client.delete('/training/set/delete/1')
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

        response = self.client.delete(
            '/training/set/delete/1'
        )
        self.assertEqual(response.json, dict(error='Отказано в доступе'))

        response = self.client.get('/logout')
        self.assertEqual(response.json, dict(response='OK'))

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        response = self.client.delete(
            '/training/set/delete/asd'
        )
        self.assertEqual(response.json, dict(error='Проверьте введеные данные!'))

        response = self.client.delete(
            '/training/set/delete/99'
        )
        self.assertEqual(response.json, dict(error='Подхода с таким ID не найдено'))

        response = self.client.delete(
            '/training/set/delete/1'
        )
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

        response = self.client.post(
            '/training/repeat/add', data=json.dumps(self.repeat_add_json_error)
        )
        self.assertEqual(response.json, dict(error='Проверьте введеные данные!'))

        response = self.client.post(
            '/training/repeat/add', data=json.dumps(self.repeat_add_set_not_exist)
        )
        self.assertEqual(response.json, dict(error='Подхода с таким ID не найдено'))

        response = self.client.post(
            '/training/repeat/add', data=json.dumps(self.repeat_add_200)
        )
        self.assertEqual(response.json, dict(response='ok'))

        response = self.client.get('/logout')
        self.assertEqual(response.json, dict(response='OK'))

        self.login(**{
            'email': 'us@er.ru',
            'password': 'useruser'
        })

        response = self.client.post(
            '/training/repeat/add', data=json.dumps(self.repeat_add_200)
        )
        self.assertEqual(response.json, dict(error='Отказано в доступе'))

    def test_repeat_edit(self):
        response = self.client.post('/training/repeat/edit', data=json.dumps({}))
        self.assert401(response)

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        response = self.client.post(
            '/training/repeat/edit', data=json.dumps(self.repeat_edit_json_error)
        )
        self.assertEqual(response.json, dict(error='Проверьте введеные данные!'))

        response = self.client.post(
            '/training/set/add', data=json.dumps(self.set200)
        )
        self.assert200(response)

        response = self.client.post(
            '/training/repeat/edit', data=json.dumps(self.repeat_edit_not_exist)
        )
        self.assertEqual(response.json, dict(error='Повтора с таким ID не найдено'))

        response = self.client.post(
            '/training/repeat/edit', data=json.dumps(self.repeat_edit_200)
        )
        self.assert200(response)

        response = self.client.get('/logout')
        self.assertEqual(response.json, dict(response='OK'))

        self.login(**{
            'email': 'us@er.ru',
            'password': 'useruser'
        })

        response = self.client.post(
            '/training/repeat/edit', data=json.dumps(self.repeat_edit_200)
        )
        self.assertEqual(response.json, dict(error='Отказано в доступе'))

    def test_repeat_delete(self):
        response = self.client.delete('/training/repeat/delete/1')
        self.assert401(response)

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        response = self.client.delete(
            '/training/repeat/delete/ads'
        )
        self.assertEqual(response.json, dict(error='Проверьте введеные данные!'))

        response = self.client.post('/training/set/add', data=json.dumps(self.set200))
        self.assert200(response)

        response = self.client.get('/logout')
        self.assertEqual(response.json, dict(response='OK'))

        self.login(**{
            'email': 'us@er.ru',
            'password': 'useruser'
        })

        response = self.client.delete(
            '/training/repeat/delete/1'
        )
        self.assertEqual(response.json, dict(error='Отказано в доступе'))

        response = self.client.get('/logout')
        self.assertEqual(response.json, dict(response='OK'))

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        response = self.client.delete(
            '/training/repeat/delete/99'
        )
        self.assertEqual(response.json, dict(error='Повтора с таким ID не найдено'))

        response = self.client.delete(
            '/training/repeat/delete/1'
        )
        self.assert200(response)

