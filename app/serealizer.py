from marshmallow import Schema, fields, post_load
from flask_marshmallow import Marshmallow
from marshmallow.fields import String
from .model import User

ma = Marshmallow()

def configure(app):
    ma.init_app(app)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance=True

class LoginSchema(Schema):
    username = fields.Str()
    password = fields.Str()

    @post_load
    def constructor(self, data, **kwargs):
        return LoginDTO(**data)

class LoginResponseSchema(Schema):
    access_token = fields.Str()
    refresh_token = fields.Str()

    @post_load
    def constructor(self, data, **kwargs):
        return LoginResponseDTO(**data)

# DTO's
    
class LoginDTO:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class LoginResponseDTO:
    def __init__(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token