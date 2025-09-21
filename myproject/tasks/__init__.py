from flask import Blueprint

# Creates the Blueprint for the 'tasks' feature
tasks_bp = Blueprint('tasks', __name__, template_folder='../templates')

# Import the routes to register them with the blueprint
# This is placed at the bottom to avoid circular dependencies
from . import views

