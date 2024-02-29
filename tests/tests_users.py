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
            cpf="12345678909"
        )

        user.hash_password()
        self.app.db.session.add(user)
        self.app.db.session.commit()

        if not hasattr(self, 'access_token'):
            self.test_login()

    def tearDown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app_context.pop()

    def test_login(self):
        with self.app.test_request_context():
            data = {
                "username": "user_test",
                "password": "password_test"
            }

            response = self.client.post(url_for("auth.login"), json=data)

            self.assertEqual(response.status_code, 200)
            self.assertIsNotNone(response.json["access_token"])
            self.access_token = response.json["access_token"]


    def test_create_user_all_valid(self):
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