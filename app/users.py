from flask import Blueprint, make_response, jsonify, request, current_app
from flask_jwt_extended import jwt_required
from .jwt_config import admin_required
from .model import User
from .serealizer import UserSchema
from .functions import validate_cpf

bp_user = Blueprint("user", __name__)

@bp_user.route("/user", methods=["POST"])
@jwt_required()
def create_user():
    try:
        us = UserSchema(exclude=('role',), unknown='exclude')
        request.get_json()["cpf"] = ''.join(filter(str.isdigit, request.get_json()["cpf"]))
        user = us.load(request.get_json())
        user.hash_password()
        if not validate_cpf(user.cpf):
            raise ValueError("Invalid CPF!")
        current_app.db.session.add(user)
        current_app.db.session.commit()
        return make_response(us.jsonify(user), 201)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@bp_user.route("/user", methods=["GET"])
@jwt_required()
@admin_required
def get_users():
    try:
        us = UserSchema(many=True)
        result = User.query.all()
        return make_response(us.jsonify(result), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


@bp_user.route("/user/<id>", methods=["GET"])
@jwt_required()
@admin_required
def get_user_by_id(id):
    try:
        us = UserSchema()
        user = User.query.get(id)
        if user is None:
            return make_response(jsonify({"error": "User not found"}), 404)
        return make_response(us.jsonify(user), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@bp_user.route("/user/<id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_user(id):
    try:
        us = UserSchema()
        user = User.query.filter_by(id=id)
        if user.first() is None:
            return make_response(jsonify({"error": "User not found"}), 404)
        user.update(request.get_json())
        current_app.db.session.commit()
        return make_response(us.jsonify(user.first()), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@bp_user.route("/user/<id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_user(id):
    try:
        us = UserSchema()
        user = User.query.filter_by(id=id)
        if user.first() is None:
            return make_response(jsonify({"error": "User not found"}), 404)
        user.update({"active": "N"})
        current_app.db.session.commit()
        return make_response(us.jsonify(user.first()), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)