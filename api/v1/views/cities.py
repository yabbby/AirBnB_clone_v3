#!/usr/bin/python3
"""Module with api routes for all City object functionality"""

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def get_cities(state_id):
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    all_cities = map(lambda city_obj: city_obj.to_dict(),
                     state.cities)
    return jsonify(list(all_cities))


@app_views.route("/cities/<city_id>", strict_slashes=False)
def get_city(city_id):
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["DELETE"])
def delete_city(city_id):
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    city.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=["POST"])
def create_city(state_id):
    body = request.get_json(silent=True)
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    if body is None:
        return make_response("Not a JSON", 400)
    if "name" not in body:
        return make_response("Missing Name", 400)

    body["state_id"] = state_id
    new_city = City(**body)
    new_city.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", strict_slashes=False,
                 methods=["PUT"])
def update_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    body = request.get_json(silent=True)
    if body is None:
        return make_response("Not a JSON", 400)

    for k, v in body.items():
        if k in ["id", "state_id", "created_at", "updated_at"]:
            continue
        setattr(city, k, v)

    city.save()

    return jsonify(city.to_dict())
