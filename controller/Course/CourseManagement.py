import pytz
from flask import (
    Blueprint,
    # Blueprint is a way to organize a group of related views and other code
    # There will be 2 blueprints: one for authentication and one for posts function
    request,
    jsonify
)

from db.oasis_entites import Course

course = Blueprint('CourseManagement', __name__, url_prefix='/course')


@course.route('/create-record', methods=['POST'])
def create():
    try:
        new_lecture = request.get_json()
        code = new_lecture.get('new_code')
        name = new_lecture.get('new_name')
        description = new_lecture.get('new_description')
        semester_id = new_lecture.get('semester_id')

        isCreated = Course.createRecord(str(code).strip(), name, description, int(semester_id))

        if isCreated is True:
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'already-exist'}), 202
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
        page_index = request.args.get('page_index')
        per_page = request.args.get('per_page')
        sort_field = request.args.get('sort_field')
        sort_order = request.args.get('sort_order')
        record = Course.getRecord(page_index, per_page, sort_field, sort_order)

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
    student_id = request.args.get('student_id')
    return jsonify({'status': 'success', 'course': Course.getStudentCourse(student_id)}), 200
