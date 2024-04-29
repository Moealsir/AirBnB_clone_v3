#!/usr/bin/python3
"""This is the user view module"""
from flask import jsonify, make_response, abort, request
from models import storage
from . import app_views
from models.user import User

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def userss():
    """ this is function users view function """
    objects_users = storage.all(User).values()
    list_of_users = []
    for us in objects_users:
        list_of_users.append(us.to_dict())
    return jsonify(list_of_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_id(user_id):
    """return data from the id"""
    us = storage.get(User, user_id)
    if not us:
        abort(404)

    return jsonify(us.to_dict())


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user_id():
    """create the user"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    dt = request.get_json()
    insta = User(**dt)
    insta.save()
    return make_response(jsonify(insta.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def state_delete(user_id):
    """delete the state"""
    us = storage.get(User, user_id)
    if not us:
        abort(404)
    storage.delete(us)
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
