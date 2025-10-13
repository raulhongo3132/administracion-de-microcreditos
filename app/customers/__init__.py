from flask import Blueprint

customers_bp = Blueprint('customers', __name__, url_prefix='/customers')

# Importación al final
from app.customers import routes