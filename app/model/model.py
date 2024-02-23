from flask_sqlalchemy import SQLAlchemy
import bcrypt

db = SQLAlchemy()

def configure(app):
    db.init_app(app)
    app.db = db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    cpf = db.Column(db.String(11), nullable=True)
    active = db.Column(db.CHAR(1), default='Y')
    role = db.Column(db.String(5), default='user')

    def hash_password(self):
        self.password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))