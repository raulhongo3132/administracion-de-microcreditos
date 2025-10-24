from flask import Blueprint, render_template, request, after_this_request
from flask_login import login_required, current_user

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Mapeo de endpoints de Flask a nombres amigables para el encabezado
ROUTE_NAMES = {
    'admin.inicio': 'Inicio',
    'admin.usuarios': 'Usuarios',
    'admin.clientes': 'Clientes',
    'admin.reportes': 'Reportes',
    'admin.prestamos': 'Préstamos',
    'admin.cuenta': 'Cuenta',
}

def get_route_name(endpoint):
    """Obtiene el nombre amigable de la ruta para el encabezado del dashboard."""
    return ROUTE_NAMES.get(endpoint, 'Panel de Administración')

@admin_bp.route('/inicio')
@login_required
def inicio():
    if not current_user.is_admin:
        return "No tienes permisos para acceder a esta página", 403
    
    # Pasa el nombre de la ruta a la plantilla
    return render_template('admin/inicio.html', 
                           route_name=get_route_name(request.endpoint))

@admin_bp.route('/usuarios')
@login_required
def usuarios():
    if not current_user.is_admin:
        return "No tienes permisos", 403
    # Pasa el nombre de la ruta y usa una plantilla placeholder
    return render_template('admin/usuarios.html', 
                           route_name=get_route_name(request.endpoint))

@admin_bp.route('/clientes')
@login_required
def clientes():
    if not current_user.is_admin:
        return "No tienes permisos", 403
    return render_template('admin/clientes.html', 
                           route_name=get_route_name(request.endpoint))

@admin_bp.route('/reportes')
@login_required
def reportes():
    if not current_user.is_admin:
        return "No tienes permisos", 403
    return render_template('admin/reportes.html', 
                           route_name=get_route_name(request.endpoint))

@admin_bp.route('/prestamos')
@login_required
def prestamos():
    if not current_user.is_admin:
        return "No tienes permisos", 403
    return render_template('admin/prestamos.html', 
                           route_name=get_route_name(request.endpoint))

@admin_bp.route('/cuenta')
@login_required
def cuenta():
    if not current_user.is_admin:
        return "No tienes permisos", 403
    return render_template('admin/cuenta.html', 
                           route_name=get_route_name(request.endpoint))

@admin_bp.after_request
def add_security_headers_admin(response):
    """
    Añade encabezados para evitar el caching de las páginas de administración, 
    solucionando el problema del botón 'Atrás' después de cerrar sesión o entrar.
    """
    # Evita que la página se almacene en caché en el historial del navegador
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    
    # Previene el "iframe-jacking" (opcional pero buena práctica)
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    
    return response

@admin_bp.before_request
@login_required
def before_admin_request():
    pass