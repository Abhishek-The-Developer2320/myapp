from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Create instances of the database and migration engine.
# These will be initialized with the Flask app in run.py.
db = SQLAlchemy()
migrate = Migrate()

