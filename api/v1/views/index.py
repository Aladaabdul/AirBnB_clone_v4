#!/usr/bin/python3
"""create route that return OK

"""
from flask import jsonify
from api.v1.views import app_views
import models
from models import storage


@app_views.route("/status", methods=['GET'])
def api_status():
    """ return JSON status: "OK"
    """
    response = {"status": "OK"}
    return jsonify(response)


@app_views.route("/stats", methods=['GET'])
def api_stat():
    """ returns the number of each objects """

    stats = {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")
            }
    return jsonify(stats)
