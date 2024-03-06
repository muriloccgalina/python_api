import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest import TestCase
from app import create_app
from flask import url_for

from app.model.model import User

class TestBase(TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()

        user = User(
            username="user_test",
            password="password_test",
            cpf="12345678909",
            role="admin"
        )

        user.hash_password()
        self.app.db.session.add(user)
        self.app.db.session.commit()

        if not hasattr(self, 'access_token'):
            self.test_login_valid()

    def tearDown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app_context.pop()

    
    # Valid tests

    def test_login_valid(self):
        with self.app.test_request_context():
            data = {
                "username": "user_test",
                "password": "password_test"
            }

            response = self.client.post(url_for("auth.login"), json=data)

            self.assertEqual(response.status_code, 200)
            self.assertIsNotNone(response.json["access_token"])
            self.access_token = response.json["access_token"]


    def test_create_user_valid(self):
        with self.app.test_request_context():
            data = {
                "username": "teste",
                "cpf": "123.456.789-09",
                "password": "teste"
            }

            response = self.client.post(url_for("user.create_user"), json=data, headers={"Authorization": f"Bearer {self.access_token}"})
            
            user = User.query.filter_by(username=data["username"]).first()
            self.assertIsNotNone(user)
            self.assertTrue(user.verify_password(data["password"]))

            response_data = response.json
            response_data.pop("id", None)
            response_data.pop("password", None)
            data.pop("password", None)
            data['cpf'] = ''.join(filter(str.isdigit, data['cpf']))
            data["active"] = "Y"

            self.assertEqual(data, response_data)

    def test_get_users_valid(self):
        with self.app.test_request_context():
            users = User.query.all()
            response = self.client.get(url_for("user.get_users"), headers={"Authorization": f"Bearer {self.access_token}"})
            self.assertEqual(response.status_code, 200)

            users_data = []
            for user in users:
                user_data = user.__dict__.copy()
                user_data.pop('_sa_instance_state', None)
                users_data.append(user_data)

            self.assertEqual(response.json, users_data)


    def test_get_user_by_id_valid(self):
        with self.app.test_request_context():
            user = User.query.filter_by(username="user_test").first()
            response = self.client.get(url_for("user.get_user_by_id", id=1), headers={"Authorization": f"Bearer {self.access_token}"})
            self.assertEqual(response.status_code, 200)
            user_data = user.__dict__
            user_data.pop('_sa_instance_state', None)
            self.assertEqual(response.json, user_data)

    def test_update_user_valid(self):
        with self.app.test_request_context():
            user_id = 1
            data = {
                "username": "updated_user",
                "cpf": "98765432100",
                "password": "updated_password"
            }
            response = self.client.put(url_for("user.update_user", id=user_id), json=data, headers={"Authorization": f"Bearer {self.access_token}"})
            self.assertEqual(response.status_code, 200)

            user = User.query.filter_by(username=data["username"]).first()
            self.assertIsNotNone(user)
            self.assertTrue(user.verify_password(data["password"]))

            response_data = response.json
            response_data.pop("id", None)
            response_data.pop("password", None)
            data.pop("password", None)
            data['cpf'] = ''.join(filter(str.isdigit, data['cpf']))
            data["active"] = "Y"
            data["role"] = "admin"

            self.assertEqual(data, response_data)


    def test_delete_user_valid(self):
        with self.app.test_request_context():
            user_id = 1
            response = self.client.delete(url_for("user.delete_user", id=user_id), headers={"Authorization": f"Bearer {self.access_token}"})
            self.assertEqual(response.status_code, 200)

            user = User.query.filter_by(id=user_id).first()
            self.assertIsNotNone(user)
            self.assertTrue(user.active == "N")

    
    # Error tests
            
    def test_create_user_error_cpf(self):
        with self.app.test_request_context():
            data = {
                "username": "teste",
                "cpf": "123.456.789-0",
                "password": "teste"
            }

            data2 = {
                "username": "teste",
                "cpf": "123.456.789009",
                "password": "teste"
            }

            data3 = {
                "username": "teste",
                "cpf": "",
                "password": "teste"
            }

            response = self.client.post(url_for("user.create_user"), json=data, headers={"Authorization": f"Bearer {self.access_token}"})
            response2 = self.client.post(url_for("user.create_user"), json=data2, headers={"Authorization": f"Bearer {self.access_token}"})
            response3 = self.client.post(url_for("user.create_user"), json=data3, headers={"Authorization": f"Bearer {self.access_token}"})

            self.assertEqual(response.status_code, 500)
            self.assertEqual(response2.status_code, 500)
            self.assertEqual(response3.status_code, 500)

    def test_create_user_error_password(self):
        with self.app.test_request_context():
            data = {
                "username": "teste",
                "cpf": "123.456.789-0",
            }

            data2 = {
                "username": "teste",
                "cpf": "123.456.789-09",
                "password": ""
            }

            response = self.client.post(url_for("user.create_user"), json=data, headers={"Authorization": f"Bearer {self.access_token}"})
            response2 = self.client.post(url_for("user.create_user"), json=data2, headers={"Authorization": f"Bearer {self.access_token}"})

            self.assertEqual(response.status_code, 500)
            self.assertEqual(response2.status_code, 500)

    def test_create_user_error_username(self):
        with self.app.test_request_context():
            data = {
                "cpf": "123.456.789-09",
                "password": "teste"
            }

            data2 = {
                "username": "",
                "cpf": "123.456.789-09",
                "password": "teste"
            }

            response = self.client.post(url_for("user.create_user"), json=data, headers={"Authorization": f"Bearer {self.access_token}"})
            response2 = self.client.post(url_for("user.create_user"), json=data2, headers={"Authorization": f"Bearer {self.access_token}"})

            self.assertEqual(response.status_code, 500)
            self.assertEqual(response2.status_code, 500)


    