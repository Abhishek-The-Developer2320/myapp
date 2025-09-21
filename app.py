from flask import Flask, render_template
from config import Config
from myproject import db, migrate
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required
from myproject.models import User
import click
# This function is the "Application Factory"
# It creates and infigures the Flask application
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app) # Initialize JWT

    # --- Register Blueprints ---
    from myproject.users.views import users_bp
    app.register_blueprint(users_bp, url_prefix='/users')

    from myproject.projects.views import projects_bp
    app.register_blueprint(projects_bp, url_prefix='/projects')
    
    from myproject.tasks.views import tasks_bp
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    @app.route('/')
    def index():
        return render_template('index.html')

    # --- A simple route for the homepage ---
    @app.context_processor
    @jwt_required(optional=True)
    def inject_user():
    # Try to get the user's ID from the login token (JWT cookie)
        
        user_id = get_jwt_identity()
        if user_id:
            # If the ID exists, find the user in the database
            user = User.query.get(int(user_id))
            return dict(current_user=user)
        # If no one is logged in, current_user will be None
        return dict(current_user=None)
    
    @app.cli.command("make-admin")
    @click.argument("username")
    def make_admin(username):
        """Gives a user admin privileges."""
    # We need an app context to interact with the database
        with app.app_context():
            user = User.query.filter_by(username=username).first()
            if user:
                user.is_admin = True
                db.session.commit()
                print(f"Success! User '{username}' has been promoted to admin.")
            else:
                print(f"Error: User '{username}' not found.")

    return app

# The entry point for running the application
if __name__ == '__main__':
    app = create_app()
    # This runs the app on http://127.0.0.1:5000 in debug mode
    app.run(debug=True)