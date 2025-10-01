#from flask import Blueprint

#bp = Blueprint('auth', __name__)

#from app.auth import routes

from flask import Blueprint

# Especificar explícitamente la carpeta de plantillas
bp = Blueprint('auth', __name__, template_folder='templates')

from app.auth import routes