#!/usr/bin/python3
"""this is the review view module"""
from flask import jsonify, abort, make_response, request
from . import app_views
from models.review import Review
from models.place import Place
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews(review_id):
    """ this is finction review view function """
    re = storage.get(Review, review_id)
    list_of_reviews = [review.
                       to_dict() for review in re.
                       reviews] if re else abort(404)
    return jsonify(list_of_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review_id(review_id):
    """return data from id"""
    re = storage.get(Review, review_id)
    return jsonify(re.to_dict()) if re else abort(404)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(review_id):
    """create the review"""
    re = storage.get(Review, review_id)
    if not re:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    if 'text' not in request.get_json():
        abort(400, description="Missing text")

    dt = request.get_json()
    insta = Review(**dt)
    insta.state_id = re.id
    insta.save()
    return make_response(jsonify(insta.to_dict()), 201)


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """delete the review"""
    re = storage.get(Review, review_id)
    storage.delete(re)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """update the review"""
    re = storage.get(Review, review_id)
    if not re:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    dt = request.get_json()
    for key, value in dt.items():
        if key not in ignore:
            setattr(re, key, value)
    storage.save()
    return make_response(jsonify(re.to_dict()), 200)
