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
import re

course = Blueprint('CourseManagement', __name__, url_prefix='/course')


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
