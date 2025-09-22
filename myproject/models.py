from myproject import db

# This file defines the structure of the database tables.

# User Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    # This establishes the one-to-many relationship with projects
    projects = db.relationship('Project', backref='author', lazy=True,cascade="all, delete-orphan")

# Project Table
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # This is the foreign key that links a project to a user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # This establishes the one-to-many relationship with tasks
    tasks = db.relationship('Task', backref='project', lazy=True, cascade="all, delete-orphan")

# Task Table
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # This is the foreign key that links a task to a project
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationship to easily access the user object
    user = db.relationship('User', backref='tasks', lazy=True)

