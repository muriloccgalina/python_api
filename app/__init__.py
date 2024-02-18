from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .model import configure as config_db
from .serealizer import configure as config_ma

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345678@localhost/pyapi_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = "secret_key"

    config_db(app)
    config_ma(app)
    
    Migrate(app, app.db)
    JWTManager(app)

    from .users import bp_user
    from .auth import bp_auth
    app.register_blueprint(bp_user)
    app.register_blueprint(bp_auth)
    
    return app