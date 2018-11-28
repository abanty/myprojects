import json
import unittest
from project.tests.base import BaseTestCase
from project import db
from project.api.models import User


def add_user(username, email, address, phone, age):
    user = User(
        username=username,
        email=email,
        address=address,
        phone=phone,
        age=age)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserService(BaseTestCase):

    def test_users(self):
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!!!', data['mensaje'])
        self.assertIn('satisfactorio', data['estado'])

    def test_add_user(self):
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'Jesus',
                    'email': 'jesusabanto@upeu.edu.pe',
                    'address': 'Alameda',
                    'phone': 'dos',
                    'age': 'veinte'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn(
                'jesusabanto@upeu.edu.pe fue agregado',
                data['mensaje'])
            self.assertIn('satisfactorio', data['estado'])

    def test_add_user_invalid_json(self):
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Carga inválida', data['mensaje'])
            self.assertIn('falló', data['estado'])

    def test_add_user_invalid_json_keys(self):
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({'email': 'jesusabanto@upeu.edu.pe'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Carga inválida.', data['mensaje'])
            self.assertIn('falló', data['estado'])

    def test_add_user_duplicate_email(self):
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'Jesus',
                    'email': 'jesusabanto@upeu.edu.pe',
                    'address': 'Alameda',
                    'phone': 'dos',
                    'age': 'veinte'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'Jesus',
                    'email': 'jesusabanto@upeu.edu.pe',
                    'address': 'Alameda',
                    'phone': 'dos',
                    'age': 'veinte'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Disculpe, ese email ya existe.', data['mensaje'])
            self.assertIn('falló', data['estado'])

    def test_single_user(self):
        user = add_user(
            'Jesus',
            'jesusabanto@upeu.edu.pe',
            'Alameda',
            'dos',
            'age')
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Jesus', data['data']['username'])
            self.assertIn('jesusabanto@upeu.edu.pe', data['data']['email'])
            self.assertIn('Alameda', data['data']['address'])
            self.assertIn('dos', data['data']['phone'])
            self.assertIn('age', data['data']['age'])
            self.assertIn('satisfactorio', data['estado'])

    def test_all_users(self):
        add_user('Jesus', 'jesusabanto@upeu.edu.pe', 'Alameda', 'dos', 'age')
        add_user(
            'Marcos',
            'examensoftware@upeu.edu.pe',
            'Huachipa',
            'cuatro',
            'as')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('Jesus', data['data']['users'][0]['username'])
            self.assertIn(
                'jesusabanto@upeu.edu.pe',
                data['data']['users'][0]['email'])
            self.assertIn('Alameda', data['data']['users'][0]['address'])
            self.assertIn('dos', data['data']['users'][0]['phone'])
            self.assertIn('age', data['data']['users'][0]['age'])
            self.assertIn('Marcos', data['data']['users'][1]['username'])
            self.assertIn(
                'examensoftware@upeu.edu.pe',
                data['data']['users'][1]['email'])
            self.assertIn('Huachipa', data['data']['users'][1]['address'])
            self.assertIn('cuatro', data['data']['users'][1]['phone'])
            self.assertIn('as', data['data']['users'][1]['age'])
            self.assertIn('satisfactorio', data['estado'])

    def test_single_user_no_id(self):
        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Usuario no existe', data['mensaje'])
            self.assertIn('fallo', data['estado'])

    def test_single_user_incorrect_id(self):
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Usuario no existe', data['mensaje'])
            self.assertIn('fallo', data['estado'])

    def test_main_no_users(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'Ingreso usuario - Arquitectura Software Abanto',
            response.data)
        self.assertIn(b'<td>No users!</td>', response.data)

    def test_main_with_users(self):
        add_user('Jesus', 'jesusabanto@upeu.edu.pe', 'Alameda', 'dos', 'age')
        add_user(
            'Marcos',
            'examensoftware@upeu.edu.pe0',
            'Huachipa',
            'cuatro',
            'as')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(
                b'Ingreso usuario - Arquitectura Software Abanto',
                response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'Jesus', response.data)
            self.assertIn(b'Marcos', response.data)

    def test_main_add_user(self):
        with self.client:
            response = self.client.post(
                '/',
                data=dict(username='Jesus', email='jesusabanto@upeu.edu.pe',
                          address='Alameda', phone='dos', age='age'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(
                b'Ingreso usuario - Arquitectura Software Abanto',
                response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'Jesus', response.data)


if __name__ == '__main__':
    unittest.main()
