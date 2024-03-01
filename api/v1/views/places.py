#!/usr/bin/python3

"""view for Place objects that handles
all default RESTFul API actions"""

from flask import request, abort, jsonify
from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place
from models.city import City
from models.state import State
from models.amenity import Amenity


@app_views.route(
        "cities/<city_id>/places",
        methods=["GET"],
        strict_slashes=False
        )
def get_places(city_id):
    """Retrives places objects"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route(
        "places/<place_id>",
        methods=["GET"],
        strict_slashes=False
        )
def get_place_id(place_id):
    """get place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        return jsonify(place.to_dict())


@app_views.route(
        "places/<place_id>",
        methods=["DELETE"],
        strict_slashes=False
        )
def delete_place(place_id):
    """Delete place object"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        srorage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route(
        "cities/<city_id>/places",
        methods=["POST"],
        strict_slashes=False
        )
def create_place(city_id):
    """Create a place object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json()
    if "user_id" not in data:
        abort(400, "Missing user_id")
    if "name" not in data:
        abort(400, "Missing name")
    user = storage(User, data["user_id"])
    if not user:
        abort(404)
    data["city_id"] = city_id
    place = Place(**data)
    place.save()
    return jsonify(city.to_dict()), 201


@app_views.route(
        "places/<place_id>",
        methods=["PUT"],
        strict_slashes=False
        )
def update_place(place_id):
    """Update place object"""
    place = storage.get(Place, place_id)
    if place:
        if not request.get_json():
            abort(400, "Not a JSON")
        data = request.get_json()
        ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
        for key, values in data.items():
            if key not in ignore_keys:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
    else:
        abort(404)
