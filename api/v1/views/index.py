#!/usr/bin/python3
""""this is the Index view module"""
from flask import jsonify
from . import app_views
from models import city, user, place, review
from models import storage, state, amenity


@app_views.route('/status', methods=['GET'])
def status():
    """Return status ok"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """return the count of stats and jsonify it"""
    stats = {
        "amenities": storage.count(amenity.Amenity),
        "cities": storage.count(city.City),
        "places": storage.count(place.Place),
        "reviews": storage.count(review.Review),
        "states": storage.count(state.State),
        "users": storage.count(user.User)
    }
    return jsonify(stats)
