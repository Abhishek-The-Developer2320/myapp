from flask import Flask, render_template
from config import Config
from myproject import db, migrate
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required
from myproject.models import User

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)


    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app) # Initialize JWT

    from myproject.users.views import users_bp
    app.register_blueprint(users_bp, url_prefix='/users')

    from myproject.projects.views import projects_bp
    app.register_blueprint(projects_bp, url_prefix='/projects')
    
    from myproject.tasks.views import tasks_bp
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    @app.route('/')
    def index():
        return render_template('index.html')

   
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

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
