#from flask import Blueprint

#bp = Blueprint('main', __name__)

#from app.main import routes

from flask import Blueprint

# Especificar explícitamente la carpeta de plantillas
bp = Blueprint('main', __name__, template_folder='templates')

from app.main import routes