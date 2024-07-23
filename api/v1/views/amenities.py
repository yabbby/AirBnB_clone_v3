#!/usr/bin/python3
"""Module with api routes for all Amenity object functionality"""

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False)
def list_amenities():
    all_amenities = map(
        lambda amenity_obj: amenity_obj.to_dict(),
        storage.all(Amenity).values())

    return jsonify(list(all_amenities))


@app_views.route("/amenities/<amenity_id>", strict_slashes=False)
def get_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route("/amenities", strict_slashes=False, methods=["POST"])
def create_amenity():
    body = request.get_json(silent=True)
    if body is None:
        return make_response("Not a JSON", 400)
    if "name" not in body:
        return make_response("Missing Name", 400)

    new_amenity = Amenity(**body)
    new_amenity.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["PUT"])
def update_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    body = request.get_json(silent=True)
    if body is None:
        return make_response("Not a JSON", 400)

    for k, v in body.items():
        if k in ["id", "created_at", "updated_at"]:
            continue
        setattr(amenity, k, v)

    amenity.save()

    return jsonify(amenity.to_dict())
