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
            user_data = User.getUser(data['sub'])
            if user_data is None:
                raise RuntimeError('User not found')
            print(user_data, flush=True)
            return f(user_data, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401  # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e, flush=True)
            return jsonify(invalid_msg), 401

    return _verify


@authentication.route('/sign-in', methods=['POST'])
def sign_in():
    user_form = request.get_json()
    username = user_form.get('username')
    check_username = re.search('[!#$%^&*()='',?";:{}|<>]', username)
    password = user_form.get('password')
    check_password = re.search('[!#$%^&*()='',?";:{}|<>]', username)
    if (check_username is None) and (check_password is None):
        check_user = User.checkUser(username, password)
        if check_user == 'Not found':
            return jsonify({'message': 'not found'}), 401
        elif check_user == 'Student':
            return jsonify({'message': 'student-unauthorized'}), 401
        else:
            token = jwt.encode({
                'sub': username,  # representing username
                'iat': datetime.utcnow(),  # issued at timestamp in seconds
                'exp': datetime.utcnow() + timedelta(minutes=480)},
                # the time in which the token will expire as seconds
                current_app.config['SECRET_KEY'])
            return jsonify({'type': check_user[1],
                            'message': 'login successful',
                            'token': token.decode('UTF-8')}), 200
    else:
        return jsonify({'message': 'unauthorized'}), 401


@authentication.route('/get-personal-data', methods=['GET'])
@token_required
def get_data(data):
    return jsonify({'user_data': data}), 200
