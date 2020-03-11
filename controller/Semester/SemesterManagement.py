import pytz
from flask import (
    Blueprint,
    # Blueprint is a way to organize a group of related views and other code
    # There will be 2 blueprints: one for authentication and one for posts function
    request,
    jsonify
)
from db.oasis_entites import Semester
from datetime import datetime

semester = Blueprint('SemesterManagement', __name__, url_prefix='/semester')


@semester.route('/create-record', methods=['POST'])
def create():
    try:
        new_lecture = request.get_json()
        name = new_lecture.get('new_name')

        isCreated = Semester.createRecord(str(name).strip())

        if isCreated is True:
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'already-exist'}), 202
    except Exception as e:
        return jsonify({'status': 'bad-request', 'error_message': e.__str__()}), 400


@semester.route('/update-record', methods=['PUT'])
def update_record():
    try:
        new_update = request.get_json()
        semester_id = new_update.get('semester_id')
        name = new_update.get('update_name')
        updated_at = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime("%Y-%m-%d %H:%M:%S")

        isUpdated = Semester.updateRecord(int(semester_id), str(name).strip(), updated_at)
        if isUpdated is True:
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'already-exist'}), 202
    except Exception as e:
        return jsonify({'status': 'bad-request', 'error_message': e.__str__()}), 400


@semester.route('/records', methods=['GET'])
def get_records():
    try:
        page_index = request.args.get('page_index')
        per_page = request.args.get('per_page')
        sort_field = request.args.get('sort_field')
        sort_order = request.args.get('sort_order')
        record = Semester.getRecord(page_index, per_page, sort_field, sort_order)

        return jsonify({
            'status': 'success',
            'records': record[0],
            'page_number': record[1].page_number,
            'page_size': record[1].page_size,
            'num_pages': record[1].num_pages,
            'total_results': record[1].total_results
        }), 200
    except Exception as e:
        return jsonify({'status': 'bad-request', 'error_message': e.__str__()}), 400


@semester.route('/all-records', methods=['GET'])
def get_all_records():
    try:
        record = Semester.getAllRecords()

        return jsonify({
            'status': 'success',
            'records': record,
        }), 200
    except Exception as e:
        return jsonify({'status': 'bad-request', 'error_message': e.__str__()}), 400


@semester.route('/search', methods=['GET'])
def search_record():
    try:
        searchSemester = request.args.get('searchSemester')
        searchRecord = Semester.searchSemesterRecord(searchSemester)

        return jsonify({
            'status': 'success',
            'search_results': searchRecord,
        }), 200
    except Exception as e:
        return jsonify({'status': 'bad-request', 'error_message': e.__str__()}), 400


@semester.route('/delete-record', methods=['DELETE'])
def delete():
    try:
        delSemester = request.get_json()
        semester_id = delSemester.get('delSemesterID')
        Semester.deleteRecord(semester_id)

        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'bad-request', 'error_message': e.__str__()}), 400
