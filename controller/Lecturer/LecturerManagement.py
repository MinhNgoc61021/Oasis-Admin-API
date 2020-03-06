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

        isCreated = User.createRecord(str(username).strip(), str(name).strip(), str(email).strip(), create_at,
                                      permission, actived, is_lock, '', '', '')
        if isCreated is True:
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'already-exist'}), 202
    except:
        return jsonify({'status': 'bad-request'}), 400


@lecturer.route('/create-lecturer-course-record', methods=['POST'])
def create_lecturer_course():
    try:
        new_lecturer_course = request.get_json()
        course_id = new_lecturer_course.get('course_id')
        user_id = new_lecturer_course.get('new_user_id')
        isCreated = Lecture.createRecordByCourse(course_id, user_id)

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

        isUpdated = Lecture.updateRecord(int(user_id), str(username).strip(), str(name).strip(), str(email).strip(),
                                         updated_at, actived, is_lock)
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


@lecturer.route('/records-by-course', methods=['GET'])
def get_records_by_course():
    try:
        course_id = request.args.get('course_id')
        page_index = request.args.get('page_index')
        per_page = request.args.get('per_page')
        sort_field = request.args.get('sort_field')
        sort_order = request.args.get('sort_order')
        record = Lecture.getRecordByCourse(course_id, page_index, per_page, sort_field, sort_order)

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
        searchRecord = Lecture.searchLecturerRecord(str(searchUsername))

        return jsonify({
            'status': 'success',
            'search_results': searchRecord,
        }), 200
    except:
        return jsonify({'status': 'bad-request'}), 400


@lecturer.route('/search-from-course', methods=['GET'])
def search_record_from_course():
    try:
        course_id = request.args.get('course_id')
        searchUsername = request.args.get('searchUsername')
        searchRecord = Lecture.searchLecturerRecordFromCourse(course_id, str(searchUsername), 'in_course')

        return jsonify({
            'status': 'success',
            'search_results': searchRecord,
        }), 200
    except:
        return jsonify({'status': 'bad-request'}), 400


@lecturer.route('/search-outside-course', methods=['GET'])
def search_record_outside_course():
    try:
        course_id = request.args.get('course_id')
        searchUsername = request.args.get('searchUsername')
        searchRecord = Lecture.searchLecturerRecordFromCourse(course_id, str(searchUsername), 'outside_course')

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


@lecturer.route('/delete-lecturer-course-record', methods=['DELETE'])
def delete_lecturer_course():
    try:
        delStudent = request.get_json()
        course_id = delStudent.get('course_id')
        user_id = delStudent.get('delUserID')
        Lecture.deleteRecordByCourse(user_id, course_id)

        return jsonify({'status': 'success'}), 200
    except:
        return jsonify({'status': 'bad-request'}), 400
