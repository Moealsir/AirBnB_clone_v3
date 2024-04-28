#!usr/bin/python3
"""this is the Amenity view module"""
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity
from . import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """return the list of all Amenity objects"""
    objects_am = storage.all(Amenity).values()
    list_of_am = []
    for am in objects_am:
        list_of_am.append(am.to_dict())
    return jsonify(list_of_am)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenities_id(amenity_id):
    """return the amenity based on the id"""
    am = storage.get(Amenity, amenity_id)
    if not am:
        abort(404)
    return jsonify(am.to_dict())


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity_id():
    """create the amenity"""
    if not request.get_json():
        print("function json check is not working")
        abort(400, description="Not a JSON")
    else:
        print("function json check is working")
    if 'name' not in request.get_json():
        print("function name check is not working")
        abort(400, description="Missing name")
    else:
        print("function name check is working")
    dt = request.get_json()
    insta = Amenity(**dt)
    insta.save()
    return make_response(jsonify(insta.to_dict()), 201)
