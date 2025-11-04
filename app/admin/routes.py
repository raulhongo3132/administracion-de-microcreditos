from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.admin.forms import UserRegistrationForm, CobradorEditForm, CuentaCobradorEditForm  
from app.models import User, CollectorAssignment, Customer
from app import db
from werkzeug.security import generate_password_hash

# Define el Blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

ROUTE_NAMES = {
    'admin.inicio': 'Inicio',
    'admin.cobradores': 'Cobradores',
    'admin.clientes': 'Clientes',
    'admin.reportes': 'Reportes',
    'admin.cuenta': 'Cuenta',
    'admin.registrar_cobrador': 'Registrar cobrador',
    'admin.editar_cobrador_form': 'Editar Cobrador',  # AGREGAR
    'admin.editar_cuenta_cobrador_form': 'Editar Cuenta',  # AGREGAR
    'admin.clientes_por_cobrador': 'Clientes del Cobrador',  # AGREGAR
}

def get_route_name(endpoint):
    return ROUTE_NAMES.get(endpoint, 'Panel de Administración')

# -------------------------------------------------------------
# Funciones Auxiliares
# -------------------------------------------------------------

def check_assignment(collector_user_id, admin_user_id):
    """Verifica si un cobrador está asignado al admin"""
    return CollectorAssignment.query.filter_by(
        admin_id=admin_user_id,
        collector_id=collector_user_id
    ).first()

def get_assigned_collectors(admin_id):
    """Obtiene todos los cobradores asignados a un admin"""
    assigned_ids = db.session.query(CollectorAssignment.collector_id).filter(
        CollectorAssignment.admin_id == admin_id
    ).subquery()
    return User.query.filter(User.id.in_(assigned_ids))

def get_customer_count_by_collector(collector_id):
    """Obtiene el número de clientes activos asignados a un cobrador"""
    return Customer.query.filter_by(
        collector_id=collector_id, 
        status=True
    ).count()

# -------------------------------------------------------------
# DECORADORES PERSONALIZADOS
# -------------------------------------------------------------

def admin_required(f):
    """Decorator para requerir permisos de admin"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            return "No tienes permisos para acceder a esta página", 403
        return f(*args, **kwargs)
    return decorated_function

# -------------------------------------------------------------
# RUTAS DE VISTA (HTML)
# -------------------------------------------------------------

@admin_bp.route('/inicio')
@login_required
@admin_required
def inicio():
    return render_template('admin/inicio.html', route_name=get_route_name(request.endpoint))

@admin_bp.route('/cobradores')
@login_required
@admin_required
def cobradores():
    usuarios = get_assigned_collectors(current_user.id).all()
    
    # Búsqueda
    query = request.args.get('q', '')
    if query:
        usuarios = [u for u in usuarios if query.lower() in u.name.lower() or 
                  (u.phone and query in u.phone)]
    
    # Contar clientes por cobrador
    for usuario in usuarios:
        usuario.clientes_asignados = get_customer_count_by_collector(usuario.id)
    
    return render_template('admin/cobradores.html', 
                         route_name=get_route_name(request.endpoint), 
                         usuarios=usuarios,
                         search_query=query)

@admin_bp.route('/clientes')
@login_required
@admin_required
def clientes():
    return render_template('admin/clientes.html', route_name=get_route_name(request.endpoint))

@admin_bp.route('/reportes')
@login_required
@admin_required
def reportes():
    return render_template('admin/reportes.html', route_name=get_route_name(request.endpoint))

@admin_bp.route('/cuenta')
@login_required
@admin_required
def cuenta():
    return render_template('admin/cuenta.html', route_name=get_route_name(request.endpoint))

@admin_bp.route('/registrar_cobrador', methods=['GET', 'POST'])
@login_required
@admin_required
def registrar_cobrador():
    form = UserRegistrationForm()
    
    # Forzar el rol a 'collector' tanto en GET como en POST
    if request.method == 'GET':
        form.rol.data = 'collector'
    
    if form.validate_on_submit():
        try:
            # Forzar el rol a collector (por si acaso)
            form.rol.data = 'collector'
            
            # Tus validaciones personalizadas ya están en el formulario
            # así que no necesitas repetirlas aquí
            
            cobrador = User(
                name=form.name.data,
                username=form.username.data,
                phone=form.phone.data,
                email=form.email.data,
                rol=form.rol.data,  # Siempre será 'collector'
                status=True
            )
            cobrador.set_password(form.password.data)
            
            db.session.add(cobrador)
            db.session.flush()
            
            asignacion = CollectorAssignment(
                admin_id=current_user.id,
                collector_id=cobrador.id
            )
            db.session.add(asignacion)
            db.session.commit()
            
            flash('Cobrador registrado y asignado con éxito.', 'success')
            return redirect(url_for('admin.cobradores'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar el cobrador: {str(e)}', 'error')
    
    return render_template('admin/registrar_cobrador.html', 
                         form=form, 
                         route_name=get_route_name(request.endpoint))

# -------------------------------------------------------------
# RUTAS PARA ACCIONES ESPECÍFICAS (HTML)
# -------------------------------------------------------------

# -------------------------------------------------------------
# RUTAS PARA FORMULARIOS DE EDICIÓN (AGREGAR ESTAS)
# -------------------------------------------------------------

@admin_bp.route('/editar_cobrador_form/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_cobrador_form(id):
    if not check_assignment(id, current_user.id):
        flash('No tienes permisos para editar este cobrador.', 'error')
        return redirect(url_for('admin.cobradores'))
    
    cobrador = User.query.get_or_404(id)
    form = CobradorEditForm()
    
    # Si es GET, llenar el formulario con los datos actuales
    if request.method == 'GET':
        form.name.data = cobrador.name
        form.phone.data = cobrador.phone
        form.email.data = cobrador.email
    
    # Si es POST, validar y guardar
    if form.validate_on_submit():
        try:
            cobrador.name = form.name.data
            cobrador.phone = form.phone.data
            cobrador.email = form.email.data
            
            db.session.commit()
            flash('Cobrador actualizado correctamente.', 'success')
            return redirect(url_for('admin.cobradores'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el cobrador: {str(e)}', 'error')
    
    return render_template('admin/editar_cobrador_form.html', 
                         form=form,
                         cobrador=cobrador,
                         route_name=get_route_name(request.endpoint))

@admin_bp.route('/editar_cuenta_cobrador_form/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_cuenta_cobrador_form(id):
    if not check_assignment(id, current_user.id):
        flash('No tienes permisos para editar este cobrador.', 'error')
        return redirect(url_for('admin.cobradores'))
    
    cobrador = User.query.get_or_404(id)
    form = CuentaCobradorEditForm()
    
    # Si es GET, llenar el formulario con los datos actuales
    if request.method == 'GET':
        form.username.data = cobrador.username
    
    # Si es POST, validar y guardar
    if form.validate_on_submit():
        try:
            if form.username.data != cobrador.username:
                # Verificar si el nuevo username ya existe
                if User.query.filter(User.username == form.username.data, User.id != id).first():
                    flash('El nombre de usuario ya está en uso.', 'error')
                    return render_template('admin/editar_cuenta_cobrador_form.html', 
                                         form=form,
                                         cobrador=cobrador,
                                         route_name=get_route_name(request.endpoint))
                cobrador.username = form.username.data
            
            if form.password.data:  # Solo actualizar si se proporcionó nueva contraseña
                cobrador.set_password(form.password.data)
            
            db.session.commit()
            flash('Credenciales actualizadas correctamente.', 'success')
            return redirect(url_for('admin.cobradores'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar las credenciales: {str(e)}', 'error')
    
    return render_template('admin/editar_cuenta_cobrador_form.html', 
                         form=form,
                         cobrador=cobrador,
                         route_name=get_route_name(request.endpoint))
    
@admin_bp.route('/actualizar_cuenta_cobrador/<int:id>', methods=['POST'])
@login_required
@admin_required
def actualizar_cuenta_cobrador(id):
    if not check_assignment(id, current_user.id):
        flash('No tienes permisos para editar este cobrador.', 'error')
        return redirect(url_for('admin.cobradores'))
    
    cobrador = User.query.get_or_404(id)
    
    try:
        nuevo_username = request.form.get('username')
        nueva_password = request.form.get('password')
        
        if nuevo_username and nuevo_username != cobrador.username:
            # Verificar si el nuevo username ya existe
            if User.query.filter(User.username == nuevo_username, User.id != id).first():
                flash('El nombre de usuario ya está en uso.', 'error')
                return redirect(url_for('admin.cobradores'))
            cobrador.username = nuevo_username
        
        if nueva_password:
            cobrador.set_password(nueva_password)
        
        db.session.commit()
        flash('Credenciales actualizadas correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al actualizar las credenciales: {str(e)}', 'error')
    
    return redirect(url_for('admin.cobradores'))

@admin_bp.route('/cambiar_estado_cobrador/<int:id>/<estado>')
@login_required
@admin_required
def cambiar_estado_cobrador(id, estado):
    if not check_assignment(id, current_user.id):
        flash('No tienes permisos para modificar este cobrador.', 'error')
        return redirect(url_for('admin.cobradores'))
    
    cobrador = User.query.get_or_404(id)
    
    try:
        if estado == 'activo':
            cobrador.status = True
            mensaje = 'Cobrador activado correctamente.'
        elif estado == 'inactivo':
            cobrador.status = False
            mensaje = 'Cobrador desactivado correctamente.'
        else:
            flash('Estado no válido.', 'error')
            return redirect(url_for('admin.cobradores'))
        
        db.session.commit()
        flash(mensaje, 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al cambiar el estado: {str(e)}', 'error')
    
    return redirect(url_for('admin.cobradores'))

@admin_bp.route('/clientes_por_cobrador/<int:id>')
@login_required
@admin_required
def clientes_por_cobrador(id):
    if not check_assignment(id, current_user.id):
        flash('No tienes permisos para ver los clientes de este cobrador.', 'error')
        return redirect(url_for('admin.cobradores'))
    
    cobrador = User.query.get_or_404(id)
    clientes = Customer.query.filter_by(
        collector_id=id, 
        status=True
    ).all()
    
    return render_template('admin/clientes_por_cobrador.html',
                         cobrador=cobrador,
                         clientes=clientes,
                         route_name=get_route_name(request.endpoint))

# -------------------------------------------------------------
# API ENDPOINTS (para AJAX/funcionalidad dinámica)
# -------------------------------------------------------------

@admin_bp.route('/api/cobradores', methods=['GET'])
@login_required
@admin_required
def get_cobradores_api():
    """API para obtener cobradores (para AJAX)"""
    cobradores = get_assigned_collectors(current_user.id).all()
    activos, inactivos = [], []

    for c in cobradores:
        customer_count = get_customer_count_by_collector(c.id)
        
        datos = {
            "id": c.id,
            "name": c.name,
            "phone": c.phone,
            "email": c.email,
            "username": c.username,
            "assigned_customers_count": customer_count,
            "status": c.status,
            "last_connection": c.last_connection.isoformat() if c.last_connection else None
        }
        if c.status:
            activos.append(datos)
        else:
            inactivos.append(datos)
            
    return jsonify({
        "active_cobradores": activos, 
        "inactive_cobradores": inactivos
    }), 200

# -------------------------------------------------------------
# MANEJADORES GLOBALES
# -------------------------------------------------------------

@admin_bp.after_request
def add_security_headers_admin(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    return response

@admin_bp.before_request
@login_required
def before_admin_request():
    """Verificación antes de cada request al admin"""
    if request.endpoint and request.endpoint.startswith('admin.'):
        if not current_user.is_admin:
            return "No tienes permisos para acceder a esta página", 403