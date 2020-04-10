import pytz
from flask import (
    Blueprint,
    # Blueprint is a way to organize a group of related views and other code
    # There will be 2 blueprints: one for authentication and one for posts function
    request,
    jsonify
)

from controller.Authentication.Authentication import token_required
from db.oasis_entites import Problem
from datetime import datetime

problem = Blueprint('ProblemManagement', __name__, url_prefix='/problem')


@problem.route('/records', methods=['GET'])
@token_required
def get_records(e):
    try:
        page_index = request.args.get('page_index')
        per_page = request.args.get('per_page')
        sort_field = request.args.get('sort_field')
        sort_order = request.args.get('sort_order')
        record = Problem.getRecord(page_index, per_page, sort_field, sort_order)

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


@problem.route('/create-record', methods=['POST'])
@token_required
def create(e):
    try:
        new_problem = request.get_json()
        title = new_problem.get('new_title')
        problem_statement = new_problem.get('new_problem_statement')
        input_format = new_problem.get('new_input_format')
        constraints = new_problem.get('new_constraints')
        output_format = new_problem.get('new_output_format')
        junit_rate = new_problem.get('new_junit_rate')
        mark_io = new_problem.get('new_mark_io')
        mark_junit = new_problem.get('new_mark_junit')
        level = new_problem.get('new_level')
        point = new_problem.get('new_point')
        submit_type = new_problem.get('new_submit_type')
        sample_code = new_problem.get('new_sample_code')
        category_id = new_problem.get('category_id')
        created_at = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime("%Y-%m-%d %H:%M:%S")
        mark_parser = new_problem.get('new_mark_parser')
        parser_rate = new_problem.get('new_parser_rate')
        isProblemCreated = Problem.createRecord(created_at, str(title).strip(), str(problem_statement).strip(),
                                                str(input_format).strip(), str(constraints).strip(),
                                                str(output_format).strip(), int(level), int(point),
                                                float(junit_rate), mark_io, int(mark_junit), int(mark_parser),
                                                float(parser_rate),
                                                submit_type, str(sample_code).strip(), category_id)
        if isProblemCreated is True:
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'already-exist'}), 202
    except Exception as e:
        return jsonify({'status': 'bad-request', 'error_message': e.__str__()}), 400


@problem.route('/update-record', methods=['PUT'])
@token_required
def update_record(e):
    try:
        update_problem = request.get_json()
        problem_id = update_problem.get('problem_id')
        update_title = update_problem.get('update_title')
        update_problem_statement = update_problem.get('update_problem_statement')
        update_input_format = update_problem.get('update_input_format')
        update_constraints = update_problem.get('update_constraints')
        update_output_format = update_problem.get('update_output_format')
        update_junit_rate = update_problem.get('update_junit_rate')
        update_mark_io = update_problem.get('update_mark_io')
        update_mark_junit = update_problem.get('update_mark_junit')
        update_level = update_problem.get('update_level')
        update_point = update_problem.get('update_point')
        update_submit_type = update_problem.get('update_submit_type')
        update_sample_code = update_problem.get('update_sample_code')
        update_category_id = update_problem.get('update_category_id')
        updated_at = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime("%Y-%m-%d %H:%M:%S")
        update_mark_parser = update_problem.get('update_mark_parser')
        update_parser_rate = update_problem.get('update_parser_rate')
        isUpdated = Problem.updateRecord(problem_id,
                                         str(update_title).strip(),
                                         str(update_problem_statement).strip(),
                                         str(update_input_format).strip(),
                                         str(update_constraints).strip(),
                                         str(update_output_format).strip(),
                                         float(update_junit_rate),
                                         update_mark_io,
                                         int(update_mark_junit),
                                         int(update_level),
                                         int(update_point),
                                         str(update_submit_type).strip(),
                                         str(update_sample_code).strip(),
                                         int(update_mark_parser),
                                         float(update_parser_rate),
                                         updated_at,
                                         update_category_id)
        if isUpdated is True:
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'already-exist'}), 202
    except Exception as e:
        return jsonify({'status': 'bad-request', 'error_message': e.__str__()}), 400


@problem.route('/delete-record', methods=['DELETE'])
@token_required
def delete(e):
    try:
        delProblem = request.get_json()
        problem_id = delProblem.get('delProblemID')
        Problem.deleteRecord(problem_id)

        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'bad-request', 'error_message': e.__str__()}), 400
