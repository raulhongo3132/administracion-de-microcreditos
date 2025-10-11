from flask import Blueprint

loan_bp = Blueprint("loan", __name__)

from . import routes
