#!/usr/bin/python3
""""this is the Index view module"""
from flask import jsonify
from . import app_views
from models import city
from models import place
from models import review
from models import user
from models import amenity
from models import state
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return status ok"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
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
