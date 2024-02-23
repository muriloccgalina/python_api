from flask import Blueprint, make_response, jsonify, request, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from ..schema.serealizer import LoginSchema, LoginResponseSchema
from ..model.model import User

bp_auth = Blueprint("auth", __name__)

@bp_auth.route("/login", methods=["POST"])
def login():
    try:
        login_obj = LoginSchema().load(request.get_json())

        user = User.query.filter_by(username=login_obj.username).first()

        if user and user.verify_password(login_obj.password):
            access_token = create_access_token(identity={"id": user.id, "username": user.username, "role": user.role})
            refresh_token = create_refresh_token(identity=user.id)
            
            lrs = LoginResponseSchema()
            response = lrs.load({"access_token": access_token, "refresh_token": refresh_token})
            return make_response(lrs.dump(response), 200)
        return make_response({"message": "Invalid credentials."}, 401)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@bp_auth.route('/refresh', methods=['POST'])
def refresh():
    try:
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return make_response(jsonify({"access_token": new_access_token}), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)