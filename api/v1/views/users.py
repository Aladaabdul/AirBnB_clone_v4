#!/usr/bin/python3
"""view for User object that handles all
default RESTFul API actions"""

from flask import jsonify, abort, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
    """Retrieve all Users"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route(
        "/users/<user_id>",
        methods=["GET"],
        strict_slashes=False
        )
def get_user_by_id(user_id):
    """Retrieve user by id"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route(
        "/users/<user_id>",
        methods=["DELETE"],
        strict_slashes=False
        )
def delete_user(user_id):
    """Delete user"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route(
        "/users",
        methods=["POST"],
        strict_slashes=False
        )
def create_user():
    """Create a new User"""
    if not request.get_json():
        abort(400, "Not a JSON")
    kwargs = request.get_json()
    if "email" not in kwargs:
        abort(400, "Missing email")
    if "password" not in kwargs:
        abort(400, "Missing password")
    user = User(**kwargs)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route(
        "/users/<user_id>",
        methods=["PUT"],
        strict_slashes=False
        )
def update_user(user_id):
    """Update a user data"""
    user = storage.get(User, user_id)
    if user:
        if not request.get_json():
            abort(400, "Not a JSON")
        data = request.get_json()
        ignore_keys = ["id", "email", "created_at", "updated_at"]
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
    else:
        abort(404)
