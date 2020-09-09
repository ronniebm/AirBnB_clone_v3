#!/usr/bin/python3
"""Status API"""

from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_s(x=None):
    """Close session at the end"""
    storage.close()

if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_PORT')

    app.run(host=host, port=port, threaded=True)
