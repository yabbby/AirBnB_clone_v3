#!/usr/bin/python3
"""Module with api routes for all State object functionality"""

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False)
def list_states():
    all_states = map(lambda state_obj: state_obj.to_dict(),
                     storage.all(State).values())

    return jsonify(list(all_states))


@app_views.route("/states", strict_slashes=False,
                 methods=["POST"])
def create_state():
    body = request.get_json(silent=True)
    if body is None:
        return make_response("Not a JSON", 400)
    if "name" not in body:
        return make_response("Missing Name", 400)

    new_state = State(**body)
    new_state.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False)
def get_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    state.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["PUT"])
def update_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    body = request.get_json(silent=True)
    if body is None:
        return make_response("Not a JSON", 400)

    for k, v in body.items():
        if k in ["id", "created_at", "updated_at"]:
            continue
        setattr(state, k, v)

    state.save()

    return jsonify(state.to_dict())
