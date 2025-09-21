from flask import Blueprint

# Creates a Blueprint object named 'users'.
# The 'template_folder' tells this blueprint where to find its HTML files.
users_bp = Blueprint('users', __name__, template_folder='../templates')

# This import is placed at the bottom to avoid circular dependency issues.
# It connects the routes defined in routes.py to this blueprint.
from . import views

