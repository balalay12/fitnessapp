import json
import unittest

from app import app, db, bcrypt
from app.mod_training.models import *
from app.mod_auth.models import User
from app.mod_anthropometry.models import Anthropometry
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


if __name__ == '__main__':
    unittest.main()
