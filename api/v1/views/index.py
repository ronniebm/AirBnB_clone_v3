#!/usr/bin/python3
"""List of states"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def api_status():
    """api_status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def some_stats():
    """Some stats"""
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Place"),
                    "states": storage.count("State"),
                    "users": storage.count("State")})
