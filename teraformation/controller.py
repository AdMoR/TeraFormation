
from __future__ import (absolute_import, division, print_function)

import json
from flask import Blueprint, jsonify, request, session
from werkzeug.wrappers import Response
from redis_query import redis_job_query, create_tag

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

    # Search in db
    job_list = redis_job_query(keyword, city)

    # If not in db parse all key to find the keyword and save the query in db
    if len(job_list) == 0:
        query = query_with_tag(keyword)
        if city and city in query.keys():
            job_list = query[city]
        else:
            job_list = None
            if not city:
                job_list = query

    code, response = 200, {'status': 'ok',
                           'status_message': 'Query went fine',
                           'data': job_list}

    return jsonify(response), code
