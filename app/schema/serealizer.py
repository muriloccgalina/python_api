from marshmallow import Schema, ValidationError, fields, post_load, validates_schema
from flask_marshmallow import Marshmallow
from ..model.model import User
from ..functions import validate_cpf

ma = Marshmallow()

def configure(app):
    ma.init_app(app)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance=True

    def load(self, data, *args, **kwargs):
        if 'cpf' in data:
            data['cpf'] = ''.join(filter(str.isdigit, data['cpf']))
        return super().load(data, *args, **kwargs)
    
    @validates_schema
    def validate_non_empty_fields(self, data, **kwargs):
        for field, value in data.items():
            if not value and field in ['username', 'password']: 
                raise ValidationError(f'{field.capitalize()} cannot be empty')
            
    @validates_schema
    def validate_fields(self, data, **kwargs):
        if 'cpf' in data:
            if not validate_cpf(data['cpf']):
                raise ValidationError('Invalid CPF!')

    def dump_skip_none(self, obj, *args, **kwargs):
        user_dict = vars(obj)
        filtered_data = {key: value for key, value in user_dict.items() if value is not None}
        return super().dump(filtered_data, *args, **kwargs)

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