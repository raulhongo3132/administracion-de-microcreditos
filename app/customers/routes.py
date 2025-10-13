from flask import Blueprint, render_template
from flask_login import login_required, current_user

customers_bp = Blueprint('customers', __name__, url_prefix='/customers')

@customers_bp.route('/')
@login_required
def dashboard():
    if not current_user.is_customer:
        return "No tienes permisos", 403
    return "Dashboard Cliente - Próximamente"

@customers_bp.route('/prestamos')
@login_required
def mis_prestamos():
    if not current_user.is_customer:
        return "No tienes permisos", 403
    return "Mis Préstamos - Próximamente"

@customers_bp.before_request
@login_required
def before_customers_request():
    pass