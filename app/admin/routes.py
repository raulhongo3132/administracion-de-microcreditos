from flask import Blueprint, render_template
from flask_login import login_required, current_user

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
def dashboard():
    # Opcional: Verificar que sea admin
    if not current_user.is_admin:
        return "No tienes permisos para acceder a esta página", 403
    return "Dashboard Admin - Próximamente"

@admin_bp.route('/clientes')
@login_required
def gestion_clientes():
    if not current_user.is_admin:
        return "No tienes permisos", 403
    return "Gestión de Clientes - Próximamente"

@admin_bp.before_request
@login_required
def before_admin_request():
    pass