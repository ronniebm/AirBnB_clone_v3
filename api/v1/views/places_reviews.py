#!/usr/bin/python3
"""
A new view for City objects that handles
all default RestFul API actions
"""
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.review import Review
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id):
    """Retrieves a list with all Review objects of a Place."""
    place_obj = storage.get('Place', place_id)

    if place_obj is None:
        abort(404)

    rev_obj = []
    rev_str = storage.all("Review")

    for key, value in rev_str.items():
        if value.place_id == str(place_id):
            rev_obj.append(value.to_dict())

    return jsonify(rev_obj)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'],
                 strict_slashes=False)
def indv_review(review_id):
    """Retrieves a Review object."""
    rev_obj = storage.get("Review", review_id)

    if rev_obj is None:
        abort(404)

    else:
        return jsonify(rev_obj.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def del_review(review_id):
    """Deletes a Review object."""

    try:
        review_obj = storage.get("Review", review_id)

        review_obj.delete()
        storage.save()
        return jsonify({}), 200

    except Exception:
        abort(404)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a Review."""

    place_obj = storage.get("Place", place_id)

    if place_obj is None:
        abort(404)

    req = request.get_json()

    if not req:
        return jsonify({"error": "Not a JSON"}), 400

    if "user_id" not in req:
        return jsonify({"error": "Missing user_id"}), 400

    user_obj = storage.get("User", req["user_id"])

    if user_obj is None:
        abort(404)

    if "text" not in req:
        return jsonify({"error": "Missing text"}), 400

    else:
        uid = req["user_id"]
        txt = req["text"]
        review = Review(user_id=uid, text=txt, place_id=place_id)

        for key, value in req.items():
            setattr(review, key, value)
        review.save()

        return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a Review object."""
    rev_obj = storage.get('Review', review_id)

    if not rev_obj:
        abort(404)

    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    classes = ["id", "place_id", "user_id", "created_at", "updated_at"]
    req = request.get_json()

    for key, val in req.items():
        if key not in classes:
            setattr(rev_obj, key, val)

    rev_obj.save()

    return (jsonify(rev_obj.to_dict()), 200)
