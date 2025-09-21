import os

# This file holds the configuration for the application.
class Config:
    # Secret key for signing cookies and JWTs. Change this to a random string.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    # Database configuration
    # IMPORTANT: Update this line with your actual PostgreSQL credentials.
    # Format: postgresql://user:password@host/dbname
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///app.db'  # Fallback to SQLite for local development
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super-secret-jwt-key'
    # Tells JWT where to look for the token (in the browser's cookies)
    JWT_TOKEN_LOCATION = ['cookies']

    JWT_COOKIE_CSRF_PROTECT = False