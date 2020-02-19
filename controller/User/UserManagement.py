import pytz
from flask import (
    Blueprint,
    # Blueprint is a way to organize a group of related views and other code
    # There will be 2 blueprints: one for authentication and one for posts function
    request,
    jsonify
)
from db.User import User
from datetime import datetime

user = Blueprint('UserManagement', __name__, url_prefix='/user')


@user.route('/records', methods=['GET'])
def get_records():
    try:
        page_index = request.args.get('page_index')
        per_page = request.args.get('per_page')
        sort_field = request.args.get('sort_field')
        sort_order = request.args.get('sort_order')
        print(request.args)
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


@user.route('/create-record', methods=['POST'])
def create():
        new_user = request.get_json()
        username = new_user.get('new_username')
        name = new_user.get('new_name')
        email = new_user.get('new_email')
        permission = new_user.get('new_permission')
        create_at = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime("%Y-%m-%d %H:%M:%S")
        actived = new_user.get('new_actived')
        is_lock = new_user.get('new_is_lock')

        isCreated = User.createRecord(username, name, email, create_at, permission, actived, is_lock)
        if isCreated is True:
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'already-exist'}), 202

@user.route('/update-record', methods=['PUT'])
def update_record():
        new_update = request.get_json()
        user_id = new_update.get('user_id')
        username = new_update.get('update_username')
        name = new_update.get('update_name')
        email = new_update.get('update_email')
        updated_at = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime("%Y-%m-%d %H:%M:%S")
        actived = new_update.get('update_actived')
        is_lock = new_update.get('update_is_lock')

        isUpdated = User.updateRecord(int(user_id), username, name, email, updated_at, actived, is_lock)
        if isUpdated is True:
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'already-exist'}), 202


@user.route('/delete-record', methods=['DELETE'])
def delete():
        delUser = request.get_json()
        ID = delUser.get('delUserID')
        print(request.get_json())
        User.deleteRecord(ID)

        return jsonify({'status': 'success'}), 200
