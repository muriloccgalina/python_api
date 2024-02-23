from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import jsonify

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user = get_jwt_identity()

            if current_user.get('role') == 'admin':
                return fn(*args, **kwargs)
            else:
                return jsonify({'message': 'Access not permitted.'}), 403
        except Exception as e:
            return jsonify({'message': 'Invalid token!'}), 401
    return wrapper
