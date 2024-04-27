#!/usr/bin/python3
"""this is the State view module"""
from flask import jsonify, abort, make_response, request
from . import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """ this is finction status view function """
    objects_states = storage.all(State).values()
    list_of_states = []
    for st in objects_states:
        list_of_states.append(st.to_dict())
    return jsonify(list_of_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_id(state_id):
    """return data from the id"""
    st = storage.get(State, state_id)
    if not st:
        abort(404)

    return jsonify(st.to_dict())


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state_id():
    """create the state"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    dt = request.get_json()
    insta = State(**dt)
    insta.save()
    return make_response(jsonify(insta.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def state_delete(state_id):
    """delete the state"""
    st = storage.get(State, state_id)
    if not st:
        abort(404)
    storage.delete(st)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """update the state"""
    st = storage.get(State, state_id)

    if not st:
        abort(404)
    if not request.get_json():
        abort(400, descritption="Not a JSON")

    discard = ['id', 'update_at', 'created_at']
    dt = request.get_json()
    for key, value in dt.items():
        if key not in discard:
            setattr(st, key, value)
    storage.save()
    return make_response(jsonify(st.to_dict()), 200)
