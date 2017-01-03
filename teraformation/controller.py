
from __future__ import (absolute_import, division, print_function)

import json
from flask import Blueprint, jsonify, request, session
from werkzeug.wrappers import Response
from teraformation.redis_query.job_query import redis_job_query, query_with_tag
import redis
import ast

api_v1 = Blueprint('teraformation', __name__)

#
# API calls handling tools
#
def format_response(response, status_code=200):
    response = Response(json.dumps(response), status=status_code,
                        mimetype='application/json')
    return response

#
# Info
#
@api_v1.route('/info', methods=['GET'])
def info():
    """Display API basic informations. Useful for Healthcheck."""
    code, response = 200, {'status': 'ok',
                           'status_message': 'everything is cool'}

    return jsonify(response), code


#
# Housekeeping endpoints
#
@api_v1.route('/get_data', methods=['GET'])
def get_data_from_db():
    """Check if layouts are healthy."""

    js = request.get_json()

    # Get main params
    city = js.get('city')
    keyword = js.get('keyword') or ''
    filters = js.get('filters') or None

    # Search in db
    r = redis.StrictRedis()
    job_list = r.hget(keyword, city)

    if job_list:
        job_list = ast.literal_eval(job_list.decode('utf-8'))

    if filters:
        temp_job_list = job_list
        job_list = []
        for job in temp_job_list:
            if 'tags' not in job.keys():
                continue
            for f in filters:
                if 'tags' in job.keys() and job['tags'] and f in job['tags']:
                    job_list.append(job)
                    break

    code, response = 200, {'status': 'ok',
                           'status_message': 'Query went fine',
                           'data': job_list}

    return jsonify(response), code
