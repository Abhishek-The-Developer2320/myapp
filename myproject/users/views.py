from flask import render_template, request, redirect, url_for, flash, make_response
from . import users_bp
from .controllers import (
    register_user, authenticate_user, get_all_users, 
    get_user_by_id, update_user, delete_user, get_dashboard_counts
)
from flask_jwt_extended import jwt_required, unset_jwt_cookies, set_access_cookies, get_jwt_identity

# This file defines the web pages (routes) for the 'users' feature.

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    
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
  
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user, access_token = authenticate_user(username, password)
        
        if access_token:
            if user.is_admin:
                redirect_url = url_for('users.admin_dashboard')
            else:
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
  
    response = make_response(redirect(url_for('index')))
    unset_jwt_cookies(response)
    flash('You have been logged out.', 'success')
    return response

@users_bp.route('/')
@jwt_required()
def list_all_users():
  
    all_users = get_all_users()
    users = sorted(all_users, key=lambda user: user.id)
    return render_template('list_users.html', users=users)

@users_bp.route('/admin-dashboard')
@jwt_required()
def admin_dashboard():
  
    current_user_id = get_jwt_identity()
    user = get_user_by_id(int(current_user_id))
    if not user or not user.is_admin:
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for('users.list_all_users'))

    counts = get_dashboard_counts()
    return render_template('admin_dashboard.html', counts=counts, current_user=user)

@users_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@jwt_required()
def edit_user(user_id):
   
    current_user_id = get_jwt_identity()
    actor = get_user_by_id(int(current_user_id))
    if not actor.is_admin:
        flash("You do not have permission to perform this action.", "danger")
        return redirect(url_for('users.list_all_users'))

    user = get_user_by_id(user_id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('users.list_all_users'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        success, message = update_user(user_id, username, email, password)
        
        if success:
            flash(message, 'success')
            return redirect(url_for('users.list_all_users'))
        else:
            flash(message, 'danger')

    return render_template('user_form.html', action='Edit', user=user)

@users_bp.route('/delete/<int:user_id>', methods=['POST'])
@jwt_required()
def delete_user_route(user_id):
 
    # Rule 1: Check if the person performing the action is an admin.
    current_user_id = get_jwt_identity()
    actor = get_user_by_id(int(current_user_id))
    if not actor.is_admin:
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('users.list_all_users'))

    # Rule 2: Prevent an admin from deleting their own account.
    if str(user_id) == current_user_id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('users.list_all_users'))
    
    # Rule 3: Prevent an admin from deleting another admin.
    user_to_delete = get_user_by_id(user_id)
    if user_to_delete and user_to_delete.is_admin:
        flash('You cannot delete another admin account.', 'danger')
        return redirect(url_for('users.list_all_users'))

    # If all checks pass, proceed with deletion.
    success = delete_user(user_id)
    if success:
        flash('User deleted successfully.', 'success')
    else:
        flash('User not found.', 'danger')
    return redirect(url_for('users.list_all_users'))

