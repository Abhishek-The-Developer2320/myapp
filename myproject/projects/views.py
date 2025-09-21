from flask import render_template, request, redirect, url_for, flash
from . import projects_bp
from .controllers import get_all_projects, create_project, get_project_by_id, update_project_by_id, delete_project_by_id
from flask_jwt_extended import jwt_required, get_jwt_identity

# This file defines the web pages (routes) for the 'projects' feature.

@projects_bp.route('/')
@jwt_required()
def list_all_projects():
    """Displays a list of all projects."""
    all_projects = get_all_projects()
    # Sort projects by ID in ascending order
    projects = sorted(all_projects, key=lambda project: project.id)
    return render_template('list_projects.html', projects=projects)

@projects_bp.route('/new', methods=['GET', 'POST'])
@jwt_required()
def add_project():
    """Handles creating a new project."""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        # Get the ID of the currently logged-in user from the JWT.
        current_user_id = get_jwt_identity()
        
        # Pass the user's ID to the controller function.
        success, message = create_project(name, description, current_user_id)
        
        if success:
            flash(message, 'success')
            return redirect(url_for('projects.list_all_projects'))
        else:
            flash(message, 'danger')

    return render_template('project_form.html', action='Add New')

@projects_bp.route('/edit/<int:project_id>', methods=['GET', 'POST'])
@jwt_required()
def edit_project(project_id):
    """Handles editing an existing project."""
    project = get_project_by_id(project_id)
    if not project:
        flash('Project not found.', 'danger')
        return redirect(url_for('projects.list_all_projects'))

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        success, message = update_project_by_id(project_id, name, description)
        
        if success:
            flash(message, 'success')
            return redirect(url_for('projects.list_all_projects'))
        else:
            flash(message, 'danger')

    return render_template('project_form.html', action='Edit', project=project)

@projects_bp.route('/delete/<int:project_id>', methods=['POST'])
@jwt_required()
def delete_project_route(project_id):
    """Handles deleting a project."""
    success, message = delete_project_by_id(project_id)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')
    return redirect(url_for('projects.list_all_projects'))

