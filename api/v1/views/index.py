#!/usr/bin/python3
""""this is the Index view module"""
from flask import jsonify
from . import app_views
from models import storage, state


@app_views.route('/status')
def status():
    """Return status ok"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """return the count of stats and jsonify it"""
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)
