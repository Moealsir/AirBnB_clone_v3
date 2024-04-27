#!/usr/bin/python3
"""this is the State view module"""
from flask import jsonify, abort, make_response, request
from . import app_views
from models import state, storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """ this is finction status view function """
    states = storage.all(state).values()
    return jsonify([state.to_dict() for state in states])
