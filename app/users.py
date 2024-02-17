from flask import Blueprint, make_response, jsonify, request, current_app
from .model import User
from .serealizer import UserSchema

bp_users = Blueprint("user", __name__)

@bp_users.route("/user", methods=["POST"])
def create_user():
    try:
        us = UserSchema()
        import pdb; pdb.set_trace()
        user = us.load(request.get_json())
        current_app.db.session.add(user)
        current_app.db.session.commit()
        return make_response(us.jsonify(user), 201)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@bp_users.route("/user", methods=["GET"])
def get_users():
    try:
        us = UserSchema(many=True)
        result = User.query.all()
        return make_response(us.jsonify(result), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


@bp_users.route("/user/<id>", methods=["GET"])
def get_user_by_id(id):
    try:
        us = UserSchema()
        user = User.query.get(id)
        if user is None:
            return make_response(jsonify({"error": "User not found"}), 404)
        return make_response(us.jsonify(user), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@bp_users.route("/user/<id>", methods=["PUT"])
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

@bp_users.route("/user/<id>", methods=["DELETE"])
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