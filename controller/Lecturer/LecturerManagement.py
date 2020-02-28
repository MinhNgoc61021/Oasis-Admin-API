import pytz
from flask import (
    Blueprint,
    # Blueprint is a way to organize a group of related views and other code
    # There will be 2 blueprints: one for authentication and one for posts function
    request,
    jsonify
)
from db.oasis_entites import Lecture
from db.oasis_entites import User
from datetime import datetime

lecturer = Blueprint('LecturerManagement', __name__, url_prefix='/lecturer')


@lecturer.route('/create-record', methods=['POST'])
def create():
    try:
        new_lecture = request.get_json()
        username = new_lecture.get('new_username')
        name = new_lecture.get('new_name')
        email = new_lecture.get('new_email')
        create_at = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime("%Y-%m-%d %H:%M:%S")
        permission = 'Giảng viên'
        actived = new_lecture.get('new_actived')
        is_lock = new_lecture.get('new_is_lock')

        isCreated = User.createRecord(str(username).strip(), str(name).strip(), str(email).strip(), create_at, permission, actived, is_lock, '', '', '', '',
                                      'LecturerForm')
        if isCreated is True:
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'already-exist'}), 202
    except:
        return jsonify({'status': 'bad-request'}), 400


@lecturer.route('/update-record', methods=['PUT'])
def update_record():
    try:
        new_update = request.get_json()
        user_id = new_update.get('user_id')
        username = new_update.get('update_username')
        name = new_update.get('update_name')
        email = new_update.get('update_email')
        updated_at = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime("%Y-%m-%d %H:%M:%S")
        actived = new_update.get('update_actived')
        is_lock = new_update.get('update_is_lock')

        isUpdated = Lecture.updateRecord(int(user_id), str(username).strip(), str(name).strip(), str(email).strip(), updated_at, actived, is_lock)
        if isUpdated is True:
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'already-exist'}), 202
    except:
        return jsonify({'status': 'bad-request'}), 400


@lecturer.route('/records', methods=['GET'])
def get_records():
    try:
        page_index = request.args.get('page_index')
        per_page = request.args.get('per_page')
        sort_field = request.args.get('sort_field')
        sort_order = request.args.get('sort_order')
        record = Lecture.getRecord(page_index, per_page, sort_field, sort_order)

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


@lecturer.route('/search', methods=['GET'])
def search_record():
    try:
        searchUsername = request.args.get('searchUsername')
        searchRecord = Lecture.searchUserRecord(str(searchUsername))

        return jsonify({
            'status': 'success',
            'search_results': searchRecord,
        }), 200
    except:
        return jsonify({'status': 'bad-request'}), 400


@lecturer.route('/delete-record', methods=['DELETE'])
def delete():
    try:
        delStudent = request.get_json()
        user_id = delStudent.get('delUserID')
        Lecture.deleteRecord(user_id)

        return jsonify({'status': 'success'}), 200
    except:
        return jsonify({'status': 'bad-request'}), 400
