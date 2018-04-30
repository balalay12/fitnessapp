import json
from tests.testconf import BaseTestCase


class ProgrammsTest(BaseTestCase):

    # data sets for add programm
    programm_add_200 = {
        'name': 'Test',
        'exercises': [1, 3]
    }

    programm_add_error_name = {
        'name': '',
        'exercises': [1]
    }

    programm_add_error_exercises = {
        'name': 'Test',
        'exercises': []
    }

    programm_add_error_exercises_not_valid = {
        'name': 'Test',
        'exercises': [1, 'adf asdf']
    }

    programm_add_error_exercises_not_exist = {
        'name': 'Test',
        'exercises': [1, 99]
    }

    # programm edit name data sets
    programm_edit_200 = {
        'id': 1,
        'name': 'rename test'
    }

    programm_edit_error = {
        'id': '',
        'name': ''
    }

    programm_edit_object_does_not_exitst = {
        'id': 3,
        'name': 'test rename'
    }

    # data sets for add exercise to programm
    exercise_add_200 = {
        'id': 1,
        'new_exercise': 2,
    }

    exercise_add_empty = {
        'id': '',
        'new_exercise': 2,
    }

    exercise_add_not_exists_programm = {
        'id': 99,
        'new_exercise': 2,
    }

    exercise_add_not_exists_exercise = {
        'id': 1,
        'new_exercise': 99,
    }

    # data sets for changing exercise in programm
    programm_change_exercise_200 = {
        'id': 1,
        'old_exercise': 1,
        'new_exercise': 2,
    }

    programm_change_empty = {
        'id': '',
        'old_exercise': 1,
        'new_exercise': 2,
    }

    programm_change_programm_not_exest = {
        'id': 3,
        'old_exercise': 1,
        'new_exercise': 2,
    }

    programm_change_exercise_not_exest = {
        'id': 1,
        'old_exercise': 4,
        'new_exercise': 4,
    }

    # data sets for delete exercise from programm
    exercise_delete_200 = {
        'id': 1,
        'exercise_id': 3
    }

    exercise_delete_error = {
        'id': '',
        'exercise_id': 3
    }

    exercise_delete_programm_does_not_exiest = {
        'id': 3,
        'exercise_id': 3
    }

    exercise_delete_exercise_does_not_exiest = {
        'id': 1,
        'exercise_id': 5
    }

    def test_add_programm(self):
        response = self.client.post('/programms/add')
        self.assert401(response)

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        response = self.client.post(
            '/programms/add',
            data=json.dumps(self.programm_add_error_name))
        self.assertEqual(response.json, dict(error='Проверьте введеные данные!'))

        response = self.client.post(
            '/programms/add',
            data=json.dumps(self.programm_add_error_exercises))
        self.assertEqual(response.json, dict(error='Не добавлено ни одного упражнения'))

        response = self.client.post(
            '/programms/add',
            data=json.dumps(self.programm_add_error_exercises_not_valid))
        self.assertEqual(response.json, dict(error='Проверьте введеные данные!'))

        response = self.client.post(
            '/programms/add',
            data=json.dumps(self.programm_add_error_exercises_not_exist))
        self.assertEqual(response.json, dict(error='Упраженния с таким ID не найдено'))

        response = self.client.post(
            '/programms/add',
            data=json.dumps(self.programm_add_200))
        self.assert200(response)

        response = self.client.get('/programms/')
        self.assert200(response)

    def test_edit_programm(self):
        response = self.client.post('/programms/edit')
        self.assert401(response)

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        response = self.client.post(
            '/programms/add',
            data=json.dumps(self.programm_add_200))
        self.assert200(response)

        response = self.client.post(
            '/programms/edit',
            data=json.dumps(self.programm_edit_error))
        self.assertEqual(response.json, dict(error='Проверьте введеные данные!'))

        response = self.client.post(
            '/programms/edit',
            data=json.dumps(self.programm_edit_object_does_not_exitst))
        self.assertEqual(response.json, dict(error='Программы с таким ID не найдено'))

        response = self.client.get('/logout')
        self.assertEqual(response.json, dict(response='OK'))

        self.login(**{
            'email': 'us@er.ru',
            'password': 'useruser'
        })

        response = self.client.post(
            '/programms/edit',
            data=json.dumps(self.programm_edit_200))
        self.assertEqual(response.json, dict(error='Отказано в доступе'))

        response = self.client.get('/logout')
        self.assertEqual(response.json, dict(response='OK'))

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        response = self.client.post(
            '/programms/edit',
            data=json.dumps(self.programm_edit_200))
        self.assert200(response)

        response = self.client.get('/programms/')
        self.assert200(response)

    def test_add_exercise(self):
        response = self.client.post('/programms/add_exercise')
        self.assert401(response)

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        response = self.client.post(
            '/programms/add',
            data=json.dumps(self.programm_add_200))
        self.assert200(response)

        response = self.client.post(
            '/programms/add_exercise',
            data=json.dumps(self.exercise_add_empty))
        self.assertEqual(response.json, dict(error='Проверьте введеные данные!'))

        response = self.client.post(
            '/programms/add_exercise',
            data=json.dumps(self.exercise_add_not_exists_programm))
        self.assertEqual(response.json, dict(error='Программы с таким ID не найдено'))

        response = self.client.post(
            '/programms/add_exercise',
            data=json.dumps(self.exercise_add_not_exists_exercise))
        self.assertEqual(response.json, dict(error='Упражнения с таким ID не найдено'))

        response = self.client.get('/logout')
        self.assertEqual(response.json, dict(response='OK'))

        self.login(**{
            'email': 'us@er.ru',
            'password': 'useruser'
        })

        response = self.client.post(
            '/programms/add_exercise',
            data=json.dumps(self.exercise_add_200))
        self.assertEqual(response.json, dict(error='Отказано в доступе'))

        response = self.client.get('/logout')
        self.assertEqual(response.json, dict(response='OK'))

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        response = self.client.post(
            '/programms/add_exercise',
            data=json.dumps(self.exercise_add_200))
        self.assert200(response)

        response = self.client.get('/programms/')
        self.assertEqual(len(response.json['programms'][0]['exercises']), 3)

    def test_change_exercise(self):
        response = self.client.post('/programms/edit_exercise')
        self.assert401(response)

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        response = self.client.post(
            '/programms/add',
            data=json.dumps(self.programm_add_200))
        self.assert200(response)

        response = self.client.post(
            '/programms/edit_exercise',
            data=json.dumps(self.programm_change_empty))
        self.assertEqual(response.json, dict(error='Проверьте введеные данные!'))

        response = self.client.post(
            '/programms/edit_exercise',
            data=json.dumps(self.programm_change_programm_not_exest))
        self.assertEqual(response.json, dict(error='Программы с таким ID не найдено'))

        response = self.client.post(
            '/programms/edit_exercise',
            data=json.dumps(self.programm_change_exercise_not_exest))
        self.assertEqual(response.json, dict(error='Упражнения с таким ID не найдено'))

        response = self.client.get('/logout')
        self.assertEqual(response.json, dict(response='OK'))

        self.login(**{
            'email': 'us@er.ru',
            'password': 'useruser'
        })

        response = self.client.post(
            '/programms/edit_exercise',
            data=json.dumps(self.programm_change_exercise_200))
        self.assertEqual(response.json, dict(error='Отказано в доступе'))

        response = self.client.get('/logout')
        self.assertEqual(response.json, dict(response='OK'))

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        response = self.client.post(
            '/programms/edit_exercise',
            data=json.dumps(self.programm_change_exercise_200))
        self.assert200(response)

        response = self.client.get('/programms/')
        self.assert200(response)

    def test_delete_exercise(self):
        response = self.client.post(
            '/programms/delete_exercise',
            data=json.dumps(self.exercise_delete_200))
        self.assert401(response)

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        response = self.client.post(
            '/programms/add',
            data=json.dumps(self.programm_add_200))
        self.assert200(response)

        response = self.client.post(
            '/programms/delete_exercise',
            data=json.dumps(self.exercise_delete_error))
        self.assertEqual(response.json, dict(error='Проверьте введеные данные!'))

        response = self.client.post(
            '/programms/delete_exercise',
            data=json.dumps(self.exercise_delete_programm_does_not_exiest))
        self.assertEqual(response.json, dict(error='Программы с таким ID не найдено'))

        response = self.client.post(
            '/programms/delete_exercise',
            data=json.dumps(self.exercise_delete_exercise_does_not_exiest))
        self.assertEqual(response.json, dict(error='Упражнения с таким ID не найдено'))

        response = self.client.get('/logout')
        self.assertEqual(response.json, dict(response='OK'))

        self.login(**{
            'email': 'us@er.ru',
            'password': 'useruser'
        })

        response = self.client.post(
            '/programms/delete_exercise',
            data=json.dumps(self.exercise_delete_200))
        self.assertEqual(response.json, dict(error='Отказано в доступе'))

        response = self.client.get('/logout')
        self.assertEqual(response.json, dict(response='OK'))

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        response = self.client.post(
            '/programms/delete_exercise',
            data=json.dumps(self.exercise_delete_200))
        self.assert200(response)

        response = self.client.get('/programms/')
        self.assert200(response)

    def test_delete_programm(self):
        response = self.client.delete('/programms/delete/1')
        self.assert401(response)

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        response = self.client.post('/programms/add', data=json.dumps(self.programm_add_200))
        self.assert200(response)

        response = self.client.delete('/programms/delete/qwer')
        self.assertEqual(response.json, dict(error='Проверьте введеные данные!'))

        response = self.client.delete('/programms/delete/99')
        self.assertEqual(response.json, dict(error='Программы с таким ID не найдено'))

        response = self.client.get('/logout')
        self.assertEqual(response.json, dict(response='OK'))

        self.login(**{
            'email': 'us@er.ru',
            'password': 'useruser'
        })

        response = self.client.delete('/programms/delete/1')
        self.assertEqual(response.json, dict(error='Отказано в доступе'))

        response = self.client.get('/logout')
        self.assertEqual(response.json, dict(response='OK'))

        self.login(**{
            'email': 'ad@min.ru',
            'password': 'adminadmin'
        })

        response = self.client.delete('/programms/delete/1')
        self.assert200(response)

        response = self.client.get('/programms/')
        self.assertEqual(len(response.json['programms']), 0)


