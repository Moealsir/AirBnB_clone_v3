#!/usr/bin/python3
"""State view module"""
from flask import jsonify, abort, make_response, request
from . import app_views
from models import state


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """ status view function """
    states = state.State.query.all()
    return jsonify([state.to_dict() for state in states])
