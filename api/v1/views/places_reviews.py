#!/usr/bin/python3

"""view for Place objects that handles
all default RESTFul API actions"""

from flask import request, abort, jsonify
from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place
from models.city import City
from models.review import Review
from models.state import State
from models.amenity import Amenity
from models.review import Review


@app_views.route(
        "places/<place_id>/reviews",
        methods=["GET"],
        strict_slashes=False
        )
def get_reviews(place_id):
    """Retrives places objects"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [place.to_dict() for place in place.reviews]
    return jsonify(reviews)


@app_views.route(
        "reviews/<review_id>",
        methods=["GET"],
        strict_slashes=False
        )
def get_review_id(review_id):
    """get review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        return jsonify(review.to_dict())


@app_views.route(
        "reviews/<review_id>",
        methods=["DELETE"],
        strict_slashes=False
        )
def delete_review(review_id):
    """Delete place object"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        srorage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route(
        "places/<place_id>/reviews",
        methods=["POST"],
        strict_slashes=False
        )
def create_review(place_id):
    """Create a place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json()
    if "user_id" not in data:
        abort(400, "Missing user_id")
    if "text" not in data:
        abort(400, "Missing name")
    user = storage(User, data["user_id"])
    if not user:
        abort(404)
    data["place_id"] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route(
        "reviews/<review_id>",
        methods=["PUT"],
        strict_slashes=False
        )
def update_review(review_id):
    """Update place object"""
    review = storage.get(Review, review_id)
    if review:
        if not request.get_json():
            abort(400, "Not a JSON")
        data = request.get_json()
        ignore_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
        for key, values in data.items():
            if key not in ignore_keys:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
    else:
        abort(404)
