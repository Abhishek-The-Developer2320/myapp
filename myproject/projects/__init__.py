from flask import Blueprint

# Creates a Blueprint object named 'projects'.
projects_bp = Blueprint('projects', __name__, template_folder='../templates')

# This import connects the routes defined in routes.py to this blueprint.
# It's placed at the bottom to avoid circular dependencies.
from . import views

