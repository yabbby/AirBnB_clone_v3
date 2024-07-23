#!/usr/bin/python3
"""Module that runs api routes"""

from os import getenv

from flask import Flask, jsonify
from flask_cors import CORS

from api.v1.views import app_views
from models import storage

app = Flask(__name__)
CORS(app, resources=r"/*", origins="0.0.0.0")

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_storage(e):
    storage.close()


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    HOST = getenv("HBNB_API_HOST") or "0.0.0.0"
    PORT = getenv("HBNB_API_PORT") or 5000
    app.run(HOST, int(PORT), threaded=True)
