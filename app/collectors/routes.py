from flask import Blueprint, render_template
from flask_login import login_required, current_user

collectors_bp = Blueprint('collectors', __name__, url_prefix='/collectors')

@collectors_bp.route('/')
@login_required
def dashboard():
    if not current_user.is_collector:
        return "No tienes permisos", 403
    return "Dashboard Cobrador - Próximamente"

@collectors_bp.route('/ruta')
@login_required
def mi_ruta():
    if not current_user.is_collector:
        return "No tienes permisos", 403
    return "Mi Ruta de Cobro - Próximamente"

@collectors_bp.before_request
@login_required
def before_collectors_request():
    pass