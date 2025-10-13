import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cambiar-en-produccion'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://usuario:contraseña@localhost/nombre_base_datos'
        # - usuario: un usuario con todos los permisos (si se complica, un superuser)
        # - contraseña: tu contraseña
        # - nombre_base_datos: depende de tu creación de tu base de datos
        #   recomiendo 'microcreditos'
    SQLALCHEMY_TRACK_MODIFICATIONS = False