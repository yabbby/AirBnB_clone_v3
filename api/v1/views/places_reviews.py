#!/usr/bin/python3
"""Module with api routes for all Review object functionality"""

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews")
def list_reviews(place_id):
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    all_reviews = map(lambda review_obj: review_obj.to_dict(),
                      place.reviews)

    return jsonify(list(all_reviews))


@app_views.route("/reviews/<review_id>", strict_slashes=False)
def get_review(review_id):
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_review(review_id):
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    review.delete()
    storage.save()
    return jsonify({})


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=["POST"])
def create_review(place_id):
    body = request.get_json(silent=True)
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    if body is None:
        return make_response("Not a JSON", 400)
    if "user_id" not in body:
        return make_response("Missing user_id", 400)

    user = storage.get(User, body.get("user_id"))

    if user is None:
        abort(404)

    if "text" not in body:
        return make_response("Missing text", 400)

    body["place_id"] = place_id
    new_review = Review(**body)
    new_review.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["PUT"])
def update_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    body = request.get_json(silent=True)
    if body is None:
        return make_response("Not a JSON", 400)

    for k, v in body.items():
        if k in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            continue
        setattr(review, k, v)

    review.save()

    return jsonify(review.to_dict())
