from unittest import TestCase
from app import create_app
from flask import url_for

class testBase(TestCase):
    def setup(self):
        self.app = create_app()
        self.app.testing = True
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.app.db.create_all()

    def tearDown(self):
        self.app.db.drop_all()


    def test_create_user(self):
        data = {
            "username": "teste",
            "cpf": "123.456.789-09",
            "password": "teste"
        }

        response = self.client.post(url_for("users.user"), json=data)

        response.json.pop(id)
        data["active"] = "Y"

        self.assertEqual(data, response.json)