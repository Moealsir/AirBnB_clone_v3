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
    for state in objects_states:
        list_of_states.append(state.to_dict())
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
        abort(400, description="Not a json")
    
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    dt = request.get_json()
    insta = State(**dt)
    insta.save()
    return make_response(jsonify(insta.to_dict()), 201)
