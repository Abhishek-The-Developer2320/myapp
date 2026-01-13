import os

class Config:

    SECRET_KEY = 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/db'  
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    JWT_SECRET_KEY =  'super-secret-jwt-key'
    JWT_TOKEN_LOCATION = ['cookies']

    JWT_COOKIE_CSRF_PROTECT = False
