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
        record = User.getRecords(page_index, per_page, sort_field, sort_order)

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
    try:
        newRoomName = request.get_json().get('newRoomName')
        newMaxcapacity = request.get_json().get('newMaxcapacity')

    except:
        return jsonify({'status': 'bad-request'}), 400


@user.route('/update-record', methods=['PUT'])
def update_student_info_record(current_user):
    try:
        new_update = request.get_json()
        user_id = new_update.get('user_id')
        username = new_update.get('update_username')
        name = new_update.get('update_name')
        email = new_update.get('update_email')
        updated_at = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime("%Y-%m-%d %H:%M:%S")
        actived = new_update.get('update_actived')
        is_lock = new_update.get('update_is_lock')

        isUpdated = User.updateRecord(user_id, username, name, email, updated_at, actived, is_lock)
        if isUpdated is True:
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'already-exist'}), 202
    except:
        return jsonify({'status': 'bad-request'}), 400

# @user.route('/remove-record', methods=['DELETE'])
# def remove:
