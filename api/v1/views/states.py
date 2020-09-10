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
    """response to 'GET'"""
    new_dict = storage.all(State)

    if request.method == 'GET':

        if state_id is None:
            states_list = []

            for key, value in new_dict.items():
                states_list.append(value.to_dict())
            return jsonify(states_list)

        else:
            for key, value in new_dict.items():
                if value.id == state_id:
                    return jsonify(value.to_dict())
            abort(404)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id=None):
    """response to 'DELETE'"""

    new_dict = storage.all(State)
    empty = {}

    if state_id is None:
        abort(404)

    for key, value in new_dict.items():

        if value.id == state_id:
            storage.delete(value)
            storage.save()
            return jsonify(empty), 200

    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """response to 'POST'"""

    new_dict = storage.all(State)
    flag = 0

    if not request.json:
        abort(400, 'Not a JSON')

    body = request.get_json()
    for key in body:
        if key == 'name':
            flag = 1

    if flag == 0:
        abort(400, "Missing name")

    new_state = State(**body)
    storage.new(new_state)
    storage.save()

    new_state_dict = new_state.to_dict()

    return jsonify(new_state_dict), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id=None):
    """response to 'PUT'"""
    new_dict = storage.all(State)

    if not request.json:
        abort(400, 'Not a JSON')

    body = request.get_json()

    for key, value in new_dict.items():

        if value.id == state_id:

            for k, v in body.items():
                setattr(value, k, v)

            storage.save()
            return jsonify(value.to_dict()), 200

    abort(404)
