#!/usr/bin/python3
"""Module with api routes for all Place object functionality"""

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def get_places(city_id):
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    all_places = map(lambda place_obj: place_obj.to_dict(),
                     city.places)

    return jsonify(list(all_places))


@app_views.route("/places/<place_id>", strict_slashes=False)
def get_place(place_id):
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_place(place_id):
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    place.delete()
    storage.save()
    return jsonify({})


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=["POST"])
def create_place(city_id):
    body = request.get_json(silent=True)
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    if body is None:
        return make_response("Not a JSON", 400)
    if "user_id" not in body:
        return make_response("Missing user_id", 400)

    user = storage.get(User, body.get("user_id"))

    if user is None:
        abort(404)

    if "name" not in body:
        return make_response("Missing name", 400)

    body["city_id"] = city_id
    new_place = Place(**body)
    new_place.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=["PUT"])
def update_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    body = request.get_json(silent=True)
    if body is None:
        return make_response("Not a JSON", 400)

    for k, v in body.items():
        if k in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            continue
        setattr(place, k, v)

    place.save()

    return jsonify(place.to_dict())
