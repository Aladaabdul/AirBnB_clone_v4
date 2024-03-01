#!/usr/bin/python3
""" A view for State objects that handles all default
    Restful API actions
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_states_id(state_id):
    """Retrieve state  object by id"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route(
        "/states/<state_id>",
        methods=["DELETE"],
        strict_slashes=False
        )
def delete_state(state_id):
    """Delete state object by id"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """Create a state object"""
    if not request.get_json:
        abort(400, "Not a JSON")
    kwargs = request.get_json()
    if "name" not in kwargs:
        abort(400, "Missing name")
    state = State(**kwargs)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            abort(400, "Not a JSON")
        data = request.get_json()
        ignore_keys = ["id", "created_at", "updated_at"]
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(404)


@app_views.errorhandler(404)
def not_found(error):
    """Handles Not Found error"""
    response = ({"error": "Not found"})
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    """Handles bad request error"""
    response = ({"error": "Bad request"})
    return jsonify(response), 400
