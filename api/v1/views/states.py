#!/usr/bin/python3
"""
A new view for State objects that handles
all default RestFul API actions
"""
from flask import abort, jsonify, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    """'GET' response"""
    dic = storage.all(State)
    if request.method == 'GET':
        if state_id is None:
            states_list = []
            for key, value in dic.items():
                states_list.append(value.to_dict())
            return jsonify(states_list)
        else:
            for key, value in dic.items():
                if value.id == state_id:
                    return jsonify(value.to_dict())
            abort(404)
