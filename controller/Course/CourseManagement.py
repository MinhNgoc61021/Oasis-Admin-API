import pytz
from flask import (
    Blueprint,
    # Blueprint is a way to organize a group of related views and other code
    # There will be 2 blueprints: one for authentication and one for posts function
    request,
    jsonify
)

from db.oasis_entites import Course
from datetime import datetime
course = Blueprint('CourseManagement', __name__, url_prefix='/course')


@course.route('/create-record', methods=['POST'])
def create():
    try:
        new_lecture = request.get_json()
        code = new_lecture.get('new_code')
        name = new_lecture.get('new_name')
        description = new_lecture.get('new_description')
        semester_id = new_lecture.get('semester_id')

        isCreated = Course.createRecord(str(code).strip(), str(name).strip(), str(description).strip(),
                                        int(semester_id))

        if isCreated is True:
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'already-exist'}), 202
    except:
        return jsonify({'status': 'bad-request'}), 400


@course.route('/update-record', methods=['PUT'])
def update_record():
    try:
        new_update = request.get_json()
        course_id = new_update.get('course_id')
        update_code = new_update.get('update_code')
        update_name = new_update.get('update_name')
        update_description = new_update.get('update_description')
        updated_at = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime("%Y-%m-%d %H:%M:%S")

        Course.updateRecord(course_id, str(update_code).strip(), str(update_name).strip(), str(update_description).strip(), updated_at)
        return jsonify({'status': 'success'}), 200
    except:
        return jsonify({'status': 'bad-request'}), 400

@course.route('/search', methods=['GET'])
def search_record():
    try:
        searchCourse = request.args.get('searchCourse')
        searchRecord = Course.searchCourseRecord(str(searchCourse))

        return jsonify({
            'status': 'success',
            'search_results': searchRecord,
        }), 200
    except:
        return jsonify({'status': 'bad-request'}), 400


@course.route('/records', methods=['GET'])
def get_records():
    try:
        semester_id = request.args.get('semester_id')
        page_index = request.args.get('page_index')
        per_page = request.args.get('per_page')
        sort_field = request.args.get('sort_field')
        sort_order = request.args.get('sort_order')
        record = Course.getRecord(semester_id, page_index, per_page, sort_field, sort_order)

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


@course.route('/student-course', methods=['GET'])
def get_student_course():
    try:
        student_id = request.args.get('student_id')
        return jsonify({'status': 'success', 'course': Course.getStudentCourse(student_id)}), 200
    except:
        return jsonify({'status': 'bad-request'}), 400


@course.route('/delete-record', methods=['DELETE'])
def delete():
    try:
        delCourse = request.get_json()
        semester_id = delCourse.get('delCourseID')
        Course.deleteRecord(semester_id)
        return jsonify({'status': 'success'}), 200
    except:
        return jsonify({'status': 'bad-request'}), 400
