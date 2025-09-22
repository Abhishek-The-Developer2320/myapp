from flask import render_template, request, flash, redirect, url_for
from . import tasks_bp
from myproject.users.controllers import get_user_by_id
from myproject.projects.controllers import get_all_projects
from .controllers import get_all_tasks, create_task, get_task_by_id, update_task, delete_task
from flask_jwt_extended import jwt_required, get_jwt_identity
from myproject.models import User

@tasks_bp.route('/')
@jwt_required()
def list_all_tasks():
    all_tasks = get_all_tasks()
    tasks = sorted(all_tasks, key=lambda task: task.id)
    projects = get_all_projects()
    return render_template('list_tasks.html', tasks=tasks, projects=projects)

@tasks_bp.route('/new', methods=['GET', 'POST'])
@jwt_required()
def add_task():
    projects = get_all_projects()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        project_id = request.form['project_id']
        current_user_id = get_jwt_identity()
        create_task(title, description, project_id, current_user_id)
        flash('Task created successfully!')
        return redirect(url_for('tasks.list_all_tasks'))
    return render_template('task_form.html', action='Add New', projects=projects)

@tasks_bp.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@jwt_required()
def edit_task(task_id):
    task = get_task_by_id(task_id)
    if not task:
        flash('Task not found!', 'danger')
        return redirect(url_for('tasks.list_all_tasks'))

    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))

    if not (user.is_admin or task.user_id == user.id):
        flash("You do not have permission to edit this task.", "danger")
        return redirect(url_for('tasks.list_all_tasks'))

    projects = get_all_projects()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        project_id = request.form['project_id']
        update_task(task_id, title, description, project_id)
        flash('Task updated successfully!')
        return redirect(url_for('tasks.list_all_tasks'))

    return render_template('task_form.html', action='Edit', task=task, projects=projects)

@tasks_bp.route('/delete/<int:task_id>', methods=['POST'])
@jwt_required()
def delete_task_route(task_id):
    task = get_task_by_id(task_id)
    if not task:
        flash('Task not found!', 'danger')
        return redirect(url_for('tasks.list_all_tasks'))

    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))

    if not (user.is_admin or task.user_id == user.id):
        flash("You do not have permission to delete this task.", "danger")
        return redirect(url_for('tasks.list_all_tasks'))

    delete_task(task_id)
    flash('Task deleted successfully!')
    return redirect(url_for('tasks.list_all_tasks'))
