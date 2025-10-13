import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cambiar-en-produccion'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://usuario:contraseña@localhost/microcreditos'
    SQLALCHEMY_TRACK_MODIFICATIONS = False