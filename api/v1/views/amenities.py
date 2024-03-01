#!/usr/bin/python3
"""A view for Amenity that handles all RESTFul API actions
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route(
        "/amenities/<amenity_id>",
        methods=["GET"],
        strict_slashes=False
        )
def amenities_by_id(amenity_id):
    """Retrieve amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route(
        "/amenities/<amenity_id>",
        methods=["DELETE"]
        )
def delete_amenity(amenity_id):
    """Delete amenity object by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route(
        "/amenities",
        methods=["POST"],
        strict_slashes=False
        )
def create_amenity():
    """Create amenity object"""
    if not request.get_json():
        abort(400, "Not a JSON")
    kwargs = request.get_json()
    if "name" not in kwargs:
        abort(400, "Missing name")
    state = Amenity(**kwargs)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route(
        "/amenities/<amenity_id>",
        methods=["PUT"],
        strict_slashes=False
        )
def update_amenity(amenity_id):
    """update amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        if not request.get_json():
            abort(400, "Not a JSON")
        data = request.get_json()
        ignore_keys = ["id", "created_at", "updated_at"]
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    else:
        abort(404)
