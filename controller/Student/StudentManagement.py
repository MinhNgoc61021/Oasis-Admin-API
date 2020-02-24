from flask import (
    Blueprint,
    # Blueprint is a way to organize a group of related views and other code
    # There will be 2 blueprints: one for authentication and one for posts function
    request,
    jsonify
)

from db.Student.StudentORM import Student
import re

student = Blueprint('StudentManagement', __name__, url_prefix='/student')


@student.route('/records', methods=['GET'])
def get_records():
    page_index = request.args.get('page_index')
    per_page = request.args.get('per_page')
    sort_field = request.args.get('sort_field')
    sort_order = request.args.get('sort_order')
    record = Student.getRecord(page_index, per_page, sort_field, sort_order)

    return jsonify({
        'status': 'success',
        'records': record[0],
        'page_number': record[1].page_number,
        'page_size': record[1].page_size,
        'num_pages': record[1].num_pages,
        'total_results': record[1].total_results
    }), 200


@student.route('/search', methods=['GET'])
def search_record():
    try:
        searchCode = request.args.get('searchCode')
        searchRecord = Student.searchUserRecord(str(searchCode))

        return jsonify({
            'status': 'success',
            'search_results': searchRecord,
        }), 200
    except:
        return jsonify({'status': 'bad-request'}), 400


@student.route('/delete-record', methods=['DELETE'])
def delete():
    try:
        delStudent = request.get_json()
        code = delStudent.get('delStudentCode')
        Student.deleteRecord(code)

        return jsonify({'status': 'success'}), 200
    except:
        return jsonify({'status': 'bad-request'}), 400
