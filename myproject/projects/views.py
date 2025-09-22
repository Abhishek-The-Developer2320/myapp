from flask import render_template, request, redirect, url_for, flash
from . import projects_bp
from .controllers import (
    get_all_projects, create_project, get_project_by_id, 
    update_project_by_id, delete_project_by_id, get_project_with_tasks
)
from flask_jwt_extended import jwt_required, get_jwt_identity
from myproject.models import User

@projects_bp.route('/')
@jwt_required()
def list_all_projects():
    """Displays a list of all projects."""
    all_projects = get_all_projects()
    projects = sorted(all_projects, key=lambda project: project.id)
    return render_template('list_projects.html', projects=projects)

@projects_bp.route('/new', methods=['POST'])
@jwt_required()
def add_project():
    """Handles creating a new project."""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        current_user_id = get_jwt_identity()
        success, message = create_project(name, description, current_user_id)
        if success:
            flash(message, 'success')
            return redirect(url_for('projects.list_all_projects'))
        else:
            flash(message, 'danger')
    return render_template('project_form.html', action='Add New')

@projects_bp.route('/edit/<int:project_id>', methods=['POST'])
@jwt_required()
def edit_project(project_id):
    """Handles editing an existing project."""
    project = get_project_by_id(project_id)
    if not project:
        flash('Project not found.', 'danger')
        return redirect(url_for('projects.list_all_projects'))

    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))

    # Permission check: admin or owner
    if not (user.is_admin or project.user_id == user.id):
        flash("You do not have permission to edit this project.", "danger")
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
    project = get_project_by_id(project_id)
    if not project:
        flash('Project not found.', 'danger')
        return redirect(url_for('projects.list_all_projects'))

    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))

    # Permission check: admin or owner
    if not (user.is_admin or project.user_id == user.id):
        flash("You do not have permission to delete this project.", "danger")
        return redirect(url_for('projects.list_all_projects'))

    success, message = delete_project_by_id(project_id)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')
    return redirect(url_for('projects.list_all_projects'))

@projects_bp.route('/<int:project_id>/tasks')
@jwt_required()
def view_project_tasks(project_id):
    """View tasks of a specific project."""
    project = get_project_by_id(project_id)
    if not project:
        flash('Project not found.', 'danger')
        return redirect(url_for('projects.list_all_projects'))
    tasks = project.tasks  # Assumes SQLAlchemy relationship 'tasks' exists

    return render_template('list_tasks.html', tasks=tasks)
