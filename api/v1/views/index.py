#!/usr/bin/python3
""""Index view module"""
from flask import jsonify
from . import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """Return status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """Return the count of each object type"""
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)


@app_views.route('/states', methods=['GET'])
def get_states():
    """Return all states objects"""
    states = states.State.query.all()
    return jsonify([state.to_dict() for state in states])
