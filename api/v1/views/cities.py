#!/usr/bin/python3
"""this is the City view module"""
from flask import jsonify, abort, make_response, request
from . import app_views
from models.city import City
from models.state import State
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET']. strict_slashes=False)
def cities(state_id):
    """ this is finction status view function """
    list_of_cities = []
    st = storage.get(State, state_id)
    list_of_cities = [city.to_dict() for city in st.cities] if st else abort(404)
    return jsonify(list_of_cities)


@app_views.route('/cities/<city_id>', methods=['GET']. strict_slashes=False)
def get_city_id(city_id):
    """return data from id"""
    st = storage.get(City, city_id)
    return jsonify(st) if st else abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(city_id):
    """create the city"""
    st = storage.get(State, city_id)
    if not st:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    dt = request.get_json()
    insta = City(**dt)
    insta.save()
    return make_response(jsonify(insta.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def city_delete(city_id):
    