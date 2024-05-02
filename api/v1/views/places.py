#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Places """
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """thet all places"""
    ct = storage.get(City, city_id)

    if not ct:
        abort(404)

    places = [place.to_dict() for place in ct.places]

    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    Retrieves place by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a place by id"""

    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    dt = request.get_json()
    user = storage.get(User, dt['user_id'])

    if not user:
        abort(404)

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    dt["city_id"] = city_id
    inst = Place(**dt)
    inst.save()
    return make_response(jsonify(inst.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """Updates a Place"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    dt = request.get_json()
    if not dt:
        abort(400, description="Not a JSON")

    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for key, value in dt.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieves Place objects based on JSON in the request body
    """

    if not request.is_json:
        abort(400, description="Request body must be in JSON format")

    data = request.json

    if not data:
        abort(400, description="Empty JSON body")

    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    if not any([states, cities, amenities]):
        places = [place.to_dict() for place in storage.all(Place).values()]
        return jsonify(places)

    list_places = []

    if states:
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    list_places.extend(city.places)

    if cities:
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                list_places.extend(city.places)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()

        amenities_objs = [storage.get(Amenity, a_id) for a_id in amenities]
        list_places = [
            place for place in list_places
            if all([amenity in place.amenities for amenity in amenities_objs])
        ]

    places = [place.to_dict(exclude=['amenities']) for place in list_places]

    return jsonify(places)
