from myproject.models import Project
from myproject import db

# This file contains the business logic for handling projects.

def get_all_projects():
    """Logic to fetch all projects."""
    return Project.query.all()

def create_project(name, description, user_id): # <-- Added user_id
    """Logic to create a new project."""
    if not name:
        return False, "Project name cannot be empty."

    # Create a new project instance, now including the user_id
    new_project = Project(
        name=name,
        description=description,
        user_id=user_id  # <-- Associate the project with the logged-in user
    )

    db.session.add(new_project)
    db.session.commit()
    
    return True, "Project created successfully."

def get_project_by_id(project_id):
    """Logic to fetch a single project by its ID."""
    return Project.query.get(project_id)

def update_project_by_id(project_id, name, description):
    """Logic to update an existing project."""
    project = get_project_by_id(project_id)
    if not project:
        return False, "Project not found."
    
    project.name = name
    project.description = description
    db.session.commit()
    
    return True, "Project updated successfully."

def delete_project_by_id(project_id):
    """Logic to delete a project."""
    project = get_project_by_id(project_id)
    if not project:
        return False, "Project not found."
        
    db.session.delete(project)
    db.session.commit()
    
    return True, "Project deleted successfully."

def get_project_with_tasks(project_id):
    """Fetch a project along with its tasks."""
    project = get_project_by_id(project_id)
    if project:
        return project.tasks  # Assumes SQLAlchemy relationship 'tasks' exists
    return []

