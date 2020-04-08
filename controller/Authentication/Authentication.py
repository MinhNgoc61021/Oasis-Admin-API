import re
from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import (
    Blueprint,
    # Blueprint is a way to organize a group of related views and other code
    # There will be 2 blueprints: one for authentication and one for posts function
    request,
    current_app,
    jsonify
)
from flask_cors import CORS

from db.oasis_entites import User

authentication = Blueprint('auth', __name__, url_prefix='/auth')
# create a blueprint is like creating a package
# ie: Sign In for authentication
CORS(authentication)


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()
        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Authentication is required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            check_user_jwt = User.getUser(data['sub'])
            if check_user_jwt is None:
                raise RuntimeError('User not found')
            print(check_user_jwt, flush=True)
            return f(check_user_jwt, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401  # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e, flush=True)
            return jsonify(invalid_msg), 401

    return _verify
