#!/usr/bin/python3
"""initliaze api"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import views after defining app_views to avoid circular import

# from api.v1.views.states import *
