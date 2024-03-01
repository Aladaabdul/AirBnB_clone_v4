#!/usr/bin/python3
"""Instance of Flask

"""
from os import getenv
from flask import jsonify
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_engine(exception):
    """method to handle teardown

    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Error Handler """
    response = {"error": "Not found"}
    return jsonify(response), 404


if __name__ == "__main__":
    HOST = getenv("HBNB_API_HOST", "0.0.0.0")
    PORT = int(getenv("HBNB_API_PORT", 5000))
    app.run(host=HOST, port=PORT, threaded=True)
