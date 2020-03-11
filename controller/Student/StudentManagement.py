import pytz
from flask import (
    Blueprint,
    # Blueprint is a way to organize a group of related views and other code
    # There will be 2 blueprints: one for authentication and one for posts function
    request,
    jsonify
)
from db.oasis_entites import Student
from db.oasis_entites import User
from pyexcel_xls import get_data
from datetime import datetime
import json

student = Blueprint('StudentManagement', __name__, url_prefix='/student')


@student.route('/create-record', methods=['POST'])
def create():
    try:
        new_student = request.get_json()
        code = new_student.get('new_code')
        username = new_student.get('new_username')
        name = new_student.get('new_name')
        email = new_student.get('new_email')
        dob = new_student.get('new_dob')
        class_cource = new_student.get('new_class_cource')
        new_course_id = new_student.get('new_course_id')
        permission = 'Sinh viên'
        create_at = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime("%Y-%m-%d %H:%M:%S")
        actived = new_student.get('new_actived')
        is_lock = new_student.get('new_is_lock')

        print(request.get_json())
        isStudentCreated = User.createRecord(str(username).strip(), str(name).strip(), str(email).strip(), create_at,
                                             str(permission).strip(), actived, is_lock, str(code).strip(), dob,
                                             str(class_cource).strip(), new_course_id)
        if isStudentCreated is True:
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'already-exist'}), 202
    except:
        return jsonify({'status': 'bad-request'}), 400


@student.route('/import-excel', methods=['POST'])
def import_excel():
    try:
        data = get_data(request.files['student_list_excel'])
        # load file
        print(json.dumps(data, ensure_ascii=False))

        return jsonify({'status': 'success'}, data), 200
    except Exception as e:
        return jsonify({'status': 'bad-request', 'error_message': e.__str__() }), 400


@student.route('/records', methods=['GET'])
def get_records():
    try:
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
    except Exception as e:
        return jsonify({'status': 'bad-request', 'error_message': e.__str__()}), 400


@student.route('/records-by-course', methods=['GET'])
def get_records_by_course():
    try:
        course_id = request.args.get('course_id')
        page_index = request.args.get('page_index')
        per_page = request.args.get('per_page')
        sort_field = request.args.get('sort_field')
        sort_order = request.args.get('sort_order')
        record = Student.getRecordByCourse(course_id, page_index, per_page, sort_field, sort_order)

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


@student.route('/search', methods=['GET'])
def search_record():
    try:
        searchCode = request.args.get('searchCode')
        searchRecord = Student.searchStudentRecord(str(searchCode))

        return jsonify({
            'status': 'success',
            'search_results': searchRecord,
        }), 200
    except Exception as e:
        return jsonify({'status': 'bad-request', 'error_message': e.__str__()}), 400


@student.route('/search-from-course', methods=['GET'])
def search_record_from_course():
    try:
        course_id = request.args.get('course_id')
        searchCode = request.args.get('searchCode')
        searchRecord = Student.searchStudentRecordFromCourse(course_id, str(searchCode), 'in_course')

        return jsonify({
            'status': 'success',
            'search_results': searchRecord,
        }), 200
    except Exception as e:
        return jsonify({'status': 'bad-request', 'error_message': e.__str__()}), 400


@student.route('/search-from-course-existence', methods=['GET'])
def search_from_course_existence():
    try:
        searchCode = request.args.get('searchCode')
        searchRecord = Student.searchStudentFromCourseExistence(str(searchCode))

        return jsonify({
            'status': 'success',
            'search_result': searchRecord,
        }), 200
    except Exception as e:
        return jsonify({'status': 'bad-request', 'error_message': e.__str__()}), 400


@student.route('/update-record', methods=['PUT'])
def update_record():
    try:
        new_update = request.get_json()
        user_id = new_update.get('user_id')
        student_id = new_update.get('student_id')
        code = new_update.get('update_code')
        username = new_update.get('update_username')
        name = new_update.get('update_name')
        email = new_update.get('update_email')
        dob = new_update.get('update_dob')
        class_course = new_update.get('update_class_course')
        course_id = new_update.get('update_course_id')
        updated_at = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime("%Y-%m-%d %H:%M:%S")
        actived = new_update.get('update_actived')
        is_lock = new_update.get('update_is_lock')

        isUpdated = Student.updateRecord(int(user_id), int(student_id), str(code).strip(), str(username).strip(),
                                         str(name).strip(), str(email).strip(), dob, str(class_course).strip(),
                                         course_id, updated_at,
                                         actived, is_lock)
        if isUpdated is True:
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'already-exist'}), 202
    except Exception as e:
        return jsonify({'status': 'bad-request', 'error_message': e.__str__()}), 400


@student.route('/delete-record', methods=['DELETE'])
def delete():
    try:
        delStudent = request.get_json()
        user_id = delStudent.get('delUserID')
        Student.deleteRecord(user_id)

        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'bad-request', 'error_message': e.__str__()}), 400


@student.route('/create-student-course-record', methods=['POST'])
def create_student_course():
    try:
        new_student_course = request.get_json()
        student_id = new_student_course.get('student_id')
        course_id = new_student_course.get('course_id')
        Student.createRecordByCourse(student_id, course_id)

        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'bad-request', 'error_message': e.__str__()}), 400


@student.route('/update-student-course-record', methods=['PUT'])
def update_student_course():
    try:
        new_student_course = request.get_json()
        student_id = new_student_course.get('student_id')
        current_course_id = new_student_course.get('current_course_id')
        update_course_id = new_student_course.get('update_course_id')
        Student.updateRecordByCourse(student_id, current_course_id, update_course_id)

        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'bad-request', 'error_message': e.__str__()}), 400


@student.route('/delete-student-course-record', methods=['DELETE'])
def delete_student_course():
    try:
        delStudent = request.get_json()
        course_id = delStudent.get('course_id')
        student_id = delStudent.get('student_id')
        Student.deleteRecordByCourse(student_id, course_id)

        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'bad-request', 'error_message': e.__str__()}), 400
