from myproject.models import User, Project, Task
from myproject import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask import jsonify

# This file contains the business logic for handling users.

def register_user(username, email, password):
    """Logic to create a new user."""
    # Check if a user with the same username or email already exists
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return False, "Username or email already exists."

    # Create a new user instance
    new_user = User(
        username=username,
        email=email,
        # We never store plain passwords. We store a "hash".
        password_hash=generate_password_hash(password)
    )

    # Add the new user to the database session and commit
    db.session.add(new_user)
    db.session.commit()
    
    return True, "User registered successfully."

def authenticate_user(username, password):
    """Logic to check user credentials and create a JWT."""
    # Find the user by their username
    user = User.query.filter_by(username=username).first()

    # Check if the user exists and the password is correct
    if user and check_password_hash(user.password_hash, password):
        # If credentials are valid, create a JWT access token.
        # The 'identity' is the data we store in the token. 
        # We explicitly convert the user's ID to a string to be safe.
        access_token = create_access_token(identity=str(user.id))
        return user,access_token
    
    return None,None

def get_all_users():
    """Logic to fetch all users from the database."""
    # This queries the User table and returns all records.
    return User.query.all()
def get_user_by_id(user_id):
    """Fetches a single user by their ID."""
    return User.query.get(user_id)
def update_user(user_id, username, email, password):
    """Updates an existing user's details."""
    user = get_user_by_id(user_id)
    if not user:
        return None, "User not found."

    # Check if the new username or email is already taken by another user
    existing_user = User.query.filter(User.id != user_id, (User.username == username) | (User.email == email)).first()
    if existing_user:
        return False, "Username or email already exists." # Return None to indicate failure due to duplicate data

    user.username = username
    user.email = email
    
    # Only update the password if a new one was provided in the form
    if password:
        user.password_hash = generate_password_hash(password)
        
    db.session.commit()
    return True, "User updated successfully."
def delete_user(user_id):
    """Deletes a user from the database."""
    user = get_user_by_id(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False    

def get_dashboard_counts():
    """Gets the total counts for users, projects, and tasks."""
    user_count = db.session.query(User).count()
    project_count = db.session.query(Project).count()
    task_count = db.session.query(Task).count()
    return {
        "users": user_count,
        "projects": project_count,
        "tasks": task_count
    }



