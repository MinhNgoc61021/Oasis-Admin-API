import pytz
from flask import (
    Blueprint,
    # Blueprint is a way to organize a group of related views and other code
    # There will be 2 blueprints: one for authentication and one for posts function
    request,
    jsonify
)

from controller.Authentication.Authentication import token_required
from db.oasis_entites import User
from db.oasis_entites import Role
from datetime import datetime

user = Blueprint('UserManagement', __name__, url_prefix='/user')


@user.route('/records', methods=['GET'])
@token_required
def get_records(e):
    try:
        page_index = request.args.get('page_index')
        per_page = request.args.get('per_page')
        sort_field = request.args.get('sort_field')
        sort_order = request.args.get('sort_order')
        record = User.getRecord(page_index, per_page, sort_field, sort_order)

        return jsonify({
            'status': 'success',
            'records': record[0],
            'page_number': record[1].page_number,
            'page_size': record[1].page_size,
            'num_pages': record[1].num_pages,
            'total_results': record[1].total_results
        }), 200
    except:
        return jsonify({'status': 'bad-request'}), 400


@user.route('/search', methods=['GET'])
@token_required
def search_record(e):
    try:
        searchUsername = request.args.get('searchUsername')
        searchRecord = User.searchUserRecord(str(searchUsername))

        return jsonify({
            'status': 'success',
            'search_results': searchRecord,
        }), 200
    except:
        return jsonify({'status': 'bad-request'}), 400


@user.route('/create-record', methods=['POST'])
@token_required
def create(e):
    try:
        new_user = request.get_json()
        username = new_user.get('new_username')
        name = new_user.get('new_name')
        email = new_user.get('new_email')
        permission = new_user.get('new_permission')
        create_at = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime("%Y-%m-%d %H:%M:%S")
        actived = new_user.get('new_actived')
        is_lock = new_user.get('new_is_lock')

        isCreated = User.createRecord(str(username).strip(), str(name).strip(), str(email).strip(), create_at,
                                      str(permission).strip(), actived, is_lock, None, None, None, None)
        if isCreated is True:
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'already-exist'}), 202
    except Exception as e:
        return jsonify({'status': 'bad-request', 'error_message': e.__str__()}), 400


@user.route('/update-record', methods=['PUT'])
@token_required
def update_record(e):
    try:
        new_update = request.get_json()
        user_id = new_update.get('user_id')
        username = new_update.get('update_username')
        name = new_update.get('update_name')
        permission = new_update.get('update_permission')
        email = new_update.get('update_email')
        updated_at = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime("%Y-%m-%d %H:%M:%S")
        actived = new_update.get('update_actived')
        is_lock = new_update.get('update_is_lock')

        isUpdated = User.updateRecord(int(user_id), str(username).strip(), str(name).strip(), str(email).strip(),
                                      updated_at, actived, is_lock, str(permission).strip())
        if isUpdated is True:
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'already-exist'}), 202
    except Exception as e:
        return jsonify({'status': 'bad-request', 'error_message': e.__str__()}), 400


@user.route('/delete-record', methods=['DELETE'])
@token_required
def delete(e):
    try:
        delUser = request.get_json()
        user_id = delUser.get('delUserID')
        User.deleteRecord(user_id)

        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'bad-request', 'error_message': e.__str__()}), 400


@user.route('/user-role', methods=['GET'])
@token_required
def getRole(e):
    try:
        user_id = request.args.get('user_id')
        return jsonify({'status': 'success', 'role_id': Role.getRecord(user_id)}), 200
    except Exception as e:
        return jsonify({'status': 'bad-request', 'error_message': e.__str__()}), 400
