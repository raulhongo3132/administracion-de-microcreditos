from flask import Blueprint

collectors_bp = Blueprint('collectors', __name__, url_prefix='/collectors')

from app.collectors import routes
