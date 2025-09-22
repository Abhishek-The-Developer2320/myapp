from flask import render_template, request, redirect, url_for, flash, make_response
from . import users_bp
from .controllers import (
    register_user, authenticate_user, get_all_users, 
    get_user_by_id, update_user, delete_user,get_dashboard_counts
)
from flask_jwt_extended import jwt_required, unset_jwt_cookies, set_access_cookies, get_jwt_identity

# This file defines the web pages (routes) for the 'users' feature.

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handles the user registration page."""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        success, message = register_user(username, email, password)
        
        if success:
            flash(message, 'success')
            return redirect(url_for('users.login'))
        else:
            flash(message, 'danger')
            
    return render_template('register.html')

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handles the user login page."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user, access_token = authenticate_user(username, password)
        
        if access_token:
            # ** THE CHANGE **: Check if the logged-in user is an admin.
            if user.is_admin:
                # If admin, redirect to the new admin dashboard.
                redirect_url = url_for('users.admin_dashboard')
            else:
                # If regular user, redirect to the normal user list.
                redirect_url = url_for('users.list_all_users')

            response = make_response(redirect(redirect_url))
            set_access_cookies(response, access_token)
            flash('Login successful!', 'success')
            return response
        else:
            flash('Invalid username or password.', 'danger')
            
    return render_template('login.html')

@users_bp.route('/logout')
@jwt_required()
def logout():
    """Handles user logout."""
    response = make_response(redirect(url_for('index')))
    unset_jwt_cookies(response)
    flash('You have been logged out.', 'success')
    return response

@users_bp.route('/')
@jwt_required()
def list_all_users():
    """Displays a list of all users."""
    all_users = get_all_users()
    users = sorted(all_users, key=lambda user: user.id)
    return render_template('list_users.html', users=users)

@users_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@jwt_required()
def edit_user(user_id):
    """Handles editing an existing user."""
    current_user_id = get_jwt_identity()
    actor= get_user_by_id(int(current_user_id))
    if actor.is_admin:
        flash("You do not have permission to edit users.", "danger")
        return redirect(url_for('users.list_all_users'))
    user = get_user_by_id(user_id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('users.list_all_users'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # ** THE FIX **: Unpack the success and message from the controller
        success, message = update_user(user_id, username, email, password)
        
        if success:
            flash(message, 'success')
            return redirect(url_for('users.list_all_users'))
        else:
            # This will now correctly flash the specific error message
            flash(message, 'danger')

    return render_template('user_form.html', action='Edit', user=user)

@users_bp.route('/delete/<int:user_id>', methods=['POST'])
@jwt_required()
def delete_user_route(user_id): # <-- **THE FIX**: Renamed function to avoid conflict
    """Handles deleting a user."""
    # Prevent a user from deleting their own account
    current_user_id = get_jwt_identity()
    actor = get_user_by_id(int(current_user_id))
    if actor and not actor.is_admin:
        flash('You do not have permission to delete users.', 'danger')
        return (redirect(url_for('users/list_all_users')))
    # Get the user object that is being targeted for deletion

    
    # Now, check if that user is an admin
    success = delete_user(user_id)
    if success:
        flash('User deleted successfully.', 'success')
    else:
        flash('User not found.', 'danger')
    return redirect(url_for('users.list_all_users'))

    # Now this correctly calls the controller function
   
@users_bp.route('/admin-dashboard')
@jwt_required()
def admin_dashboard():
    """Displays the admin-only dashboard with counts."""
    current_user_id = get_jwt_identity()
    current_user = get_user_by_id(int(current_user_id))
    if not current_user or not current_user.is_admin:
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for('users.list_all_users'))
    counts = get_dashboard_counts()
    return render_template('admin_dashboard.html', counts=counts,current_user=current_user)
