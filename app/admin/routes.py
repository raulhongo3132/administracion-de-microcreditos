from flask import Blueprint, render_template, request, after_this_request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.admin.forms import UserRegistrationForm
from app.models import User
from app import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Mapeo de endpoints de Flask a nombres amigables para el encabezado
ROUTE_NAMES = {
    'admin.inicio': 'Inicio',
    'admin.usuarios': 'Usuarios',
    'admin.clientes': 'Clientes',
    'admin.reportes': 'Reportes',
    'admin.cuenta': 'Cuenta',
    'admin.registrar_cobrador': 'Registrar cobrador',
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

@admin_bp.route('/cobradores')
@login_required
def cobradores():
    if not current_user.is_admin:
        return "No tienes permisos", 403
    
    usuarios = User.query.all()
    
    return render_template('admin/cobradores.html', 
                           route_name=get_route_name(request.endpoint),
                           usuarios=usuarios)

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

@admin_bp.route('/cuenta')
@login_required
def cuenta():
    if not current_user.is_admin:
        return "No tienes permisos", 403
    return render_template('admin/cuenta.html', 
                           route_name=get_route_name(request.endpoint))

@admin_bp.route('/registrar_cobrador', methods=['GET', 'POST'])
@login_required
def registrar_cobrador():
    if not current_user.is_admin:
        flash('No tienes permisos para acceder a esta página.', 'error')
        return redirect(url_for('admin.inicio'))
    
    form = UserRegistrationForm()
    
    if request.method == 'GET':
        form.rol.data = 'collector'
    
    if form.validate_on_submit():
        try:
            # Crear el nuevo usuario
            user = User(
                name=form.name.data,
                username=form.username.data,
                phone=form.phone.data,
                email=form.email.data,
                rol=form.rol.data
            )
            user.set_password(form.password.data)
            
            db.session.add(user)
            db.session.commit()
            
            return redirect(url_for('admin.usuarios'))  # Redirigir a la lista de usuarios
            
        except Exception as e:
            db.session.rollback()
            flash('Error al registrar el usuario. Intenta nuevamente.', 'error')
    
    # Pasa el nombre de la ruta a la plantilla
    return render_template('admin/registrar_cobrador.html', 
                           form=form,
                           route_name=get_route_name(request.endpoint))

@admin_bp.after_request
def add_security_headers_admin(response):
    """
    Añade encabezados para evitar el caching de las páginas de administración, 
    solucionando el problema del botón 'Atrás' después de cerrar sesión o entrar.
    """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    
    return response

@admin_bp.before_request
@login_required
def before_admin_request():
    pass