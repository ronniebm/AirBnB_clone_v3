#!/usr/bin/python3
"""Init file"""
from api.v1.views.index import *
from flask import Blueprint
from models.state import State
from api.v1.views.states import *


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
