# app/user_profile/__init__.py

from flask import Blueprint

user_profile = Blueprint('user_profile', __name__)

from . import views