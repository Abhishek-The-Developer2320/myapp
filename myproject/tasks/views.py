from flask import render_template, request, flash, redirect, url_for
from . import tasks_bp
from .controllers import (
    get_all_tasks, 
    create_task, 
    get_task_by_id, 
    update_task, 
    delete_task
)
# We need to get projects for the dropdown menu in the task form
from myproject.projects.controllers import get_all_projects
from flask_jwt_extended import jwt_required

# This file defines the URL routes for the tasks feature.

@tasks_bp.route('/')
@jwt_required()
def list_all_tasks():
    """Route to display all tasks, sorted by ID."""
    all_tasks = get_all_tasks()
    # Sort the tasks by ID in ascending order
    tasks = sorted(all_tasks, key=lambda task: task.id)
    projects = get_all_projects() # Needed for the form if it's on the same page
    return render_template('list_tasks.html', tasks=tasks, projects=projects)

@tasks_bp.route('/new', methods=['GET', 'POST'])
@jwt_required()
def add_task():
    """Route to handle adding a new task."""
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        project_id = request.form['project_id']
        create_task(title, description, project_id)
        flash('Task created successfully!')
        return redirect(url_for('tasks.list_all_tasks'))
    
    # Provide the list of projects to the form template for the dropdown
    projects = get_all_projects()
    return render_template('task_form.html', action='Add New', projects=projects)

@tasks_bp.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@jwt_required()
def edit_task(task_id):
    """Route to handle editing an existing task."""
    task = get_task_by_id(task_id)
    if not task:
        flash('Task not found!')
        return redirect(url_for('tasks.list_all_tasks'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        project_id = request.form['project_id']
        update_task(task_id, title, description, project_id)
        flash('Task updated successfully!')
        return redirect(url_for('tasks.list_all_tasks'))
    
    projects = get_all_projects()
    return render_template('task_form.html', action='Edit', task=task, projects=projects)

@tasks_bp.route('/delete/<int:task_id>', methods=['POST'])
@jwt_required()
def delete_task_route(task_id):
    """Route to handle deleting a task."""
    success = delete_task(task_id)
    if success:
        flash('Task deleted successfully.')
    else:
        flash('Task not found.')
    return redirect(url_for('tasks.list_all_tasks'))

