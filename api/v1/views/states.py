#!/usr/bin/python3
"""State view module"""
from flask import jsonify
from . import app_views
from models import storage, state

# @app_views.route('/states', methods=['GET'])
# def get_states():
#     """Return all states objects"""
#     return jsonify({"status": "OK"})