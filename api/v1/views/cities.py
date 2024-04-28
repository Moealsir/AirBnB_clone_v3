#!/usr/bin/python3
"""this is the City view module"""
from flask import jsonify, abort, make_response, request
from . import app_views
from models.city import City
from models.state import State
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities(state_id):
    """ this is finction status view function """
    st = storage.get(State, state_id)
    list_of_cities = [city.to_dict()
                      for city in st.cities] if st else abort(404)
    return jsonify(list_of_cities)


@app_views.route('/cities/<city_id>/', methods=['GET'],
                 strict_slashes=False)
def get_city_id(city_id):
    """return data from id"""
    ct = storage.get(City, city_id)
    return jsonify(ct.to_dict()) if ct else abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """create the city"""
    st = storage.get(State, state_id)
    if not st:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    dt = request.get_json()
    insta = City(**dt)
    insta.state_id = st.id
    insta.save()
    return make_response(jsonify(insta.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """delete the city"""
    ct = storage.get(City, city_id)
    storage.delete(ct)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """update the city"""
    ct = storage.get(City, city_id)
    if not ct:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    dt = request.get_json()
    for key, value in dt.items():
        if key not in ignore:
            setattr(ct, key, value)
    storage.save()
    return make_response(jsonify(ct.to_dict()), 200)
