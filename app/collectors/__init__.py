from flask import Blueprint

collectors_bp = Blueprint('collectors', __name__, url_prefix='/collectors')

# Importación al final
from app.collectors import routes
