from flask import Blueprint

collector_bp = Blueprint("collector", __name__)

from . import routes
