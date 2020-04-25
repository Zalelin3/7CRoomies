<<<<<<< HEAD
# app/user_profile/__init__.py
=======
# app/profile/__init__.py
>>>>>>> e8397d5e69eff73d37dbc9cc1607ee97f9901d9e

from flask import Blueprint

profile = Blueprint('profile', __name__)

from . import views