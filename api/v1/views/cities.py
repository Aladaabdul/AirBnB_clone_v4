#!/usr/bin/python3
"""View for City objects that handles
    all default RESTFul API actions
    """""

from flask import abort, jsonify, request
from models.state import State
from models.city import City
from api.v1.views import app_views
from models import storage
import models


@app_views.route(
        "/states/<state_id>/cities",
        methods=["GET"],
        strict_slashes=False
        )
def get_cities_by_state(state_id):
    """Retrieve city by state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """Retrieve city by id"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route(
        "/cities/<city_id>",
        methods=["DELETE"]
        )
def delete_city(city_id):
    """Delete state by id"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route(
        "/states/<state_id>/cities",
        methods=["POST"],
        strict_slashes=False
        )
def create_city(state_id):
    """Create city object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json()
    if "name" not in data:
        abort(400, "Not a JSON")
    data["state_id"] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route(
        "/cities/<city_id>",
        methods=["PUT"],
        strict_slashes=False
        )
def update_city(city_id):
    city = storage.get(City, city_id)
    if city:
        if not request.get_json():
            abort(400, "Not a Json")
        data = request.get_json()
        ignore_keys = ["id", "state_id", "created_at", "updated_at"]
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
    else:
        abort(404)


@app_views.errorhandler(404)
def not_found(error):
    """Handles not found error"""
    response = ({"error": "Not found"})
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    """Bad request error"""
    response = ({"error": "Bad request"})
    return jsonify(response), 400
