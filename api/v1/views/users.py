#!/usr/bin/python3
"""Module with api routes for all User object functionality"""

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False)
def list_users():
    all_amenities = map(
        lambda user_obj: user_obj.to_dict(),
        storage.all(User).values())

    return jsonify(list(all_amenities))


@app_views.route("/users/<user_id>", strict_slashes=False)
def get_user(user_id):
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    user.delete()
    storage.save()
    return jsonify({})


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def create_user():
    body = request.get_json(silent=True)
    if body is None:
        return make_response("Not a JSON", 400)
    if "email" not in body:
        return make_response("Missing email", 400)
    if "password" not in body:
        return make_response("Missing password", 400)

    new_user = User(**body)
    new_user.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=["PUT"])
def update_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    body = request.get_json(silent=True)
    if body is None:
        return make_response("Not a JSON", 400)

    for k, v in body.items():
        if k in ["id", "email", "created_at", "updated_at"]:
            continue
        setattr(user, k, v)

    user.save()

    return jsonify(user.to_dict())
