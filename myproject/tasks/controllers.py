from myproject.models import Task
from myproject import db

# This file contains the business logic for the tasks feature.
# It directly interacts with the database.

def get_all_tasks():
    """Fetches all tasks from the database."""
    return Task.query.all()

def get_task_by_id(task_id):
    """Fetches a single task by its ID."""
    return Task.query.get(task_id)

def create_task(title, description, project_id,user_id):
    """Creates a new task and saves it to the database."""
    new_task = Task(title=title, description=description, project_id=project_id,user_id=user_id)
    db.session.add(new_task)
    db.session.commit()
    return new_task

def update_task(task_id, title, description, project_id):
    """Updates an existing task in the database."""
    task = get_task_by_id(task_id)
    if task:
        task.title = title
        task.description = description
        task.project_id = project_id
        db.session.commit()
    return task

def delete_task(task_id):
    """Deletes a task from the database."""
    task = get_task_by_id(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return True
    return False

