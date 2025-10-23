from flask import Blueprint, render_template, request, after_this_request
from flask_login import login_required, current_user

collectors_bp = Blueprint('collectors', __name__, url_prefix='/collectors')

ROUTE_NAMES = {
    'collectors.inicio': 'Inicio',
    'collectors.usuarios': 'Usuarios',
    'collectors.clientes': 'Clientes',
    'collectors.reportes': 'Reportes',
    'collectors.prestamos': 'Préstamos',
    'collectors.cuenta': 'Cuenta',
}

def get_route_name(endpoint):
    return ROUTE_NAMES.get(endpoint, 'Panel de Cobro')

@collectors_bp.route('/inicio')
@login_required
def inicio():
    if not current_user.is_collector:
        return "No tienes permisos para acceder a esta página", 403
    
    # Pasa el nombre de la ruta a la plantilla
    return render_template('collectors/inicio.html', 
                           route_name=get_route_name(request.endpoint))

@collectors_bp.route('/clientes')
@login_required
def clientes():
    if not current_user.id_collector:
        return "No tienes permisos", 403
    return render_template('collectors/placeholder.html', 
                           route_name=get_route_name(request.endpoint))

@collectors_bp.route('/reportes')
@login_required
def reportes():
    if not current_user.is_collector:
        return "No tienes permisos", 403
    return render_template('collectors/placeholder.html', 
                           route_name=get_route_name(request.endpoint))

@collectors_bp.route('/cuenta')
@login_required
def cuenta():
    if not current_user.is_collector:
        return "No tienes permisos", 403
    return render_template('collectors/placeholder.html', 
                           route_name=get_route_name(request.endpoint))

@collectors_bp.after_request
def add_security_headers_collector(response):
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

@collectors_bp.before_request
@login_required
def before_collectors_request():
    pass