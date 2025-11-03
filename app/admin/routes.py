from flask import Blueprint, render_template, request, after_this_request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.admin.forms import UserRegistrationForm
from app.models import User, CollectorAssignment # Importa la clase de asignación
from app import db
from werkzeug.security import generate_password_hash

# Define el Blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Mapeo de endpoints de Flask a nombres amigables para el encabezado
ROUTE_NAMES = {
    'admin.inicio': 'Inicio',
    'admin.cobradores': 'Cobradores',
    'admin.clientes': 'Clientes',
    'admin.reportes': 'Reportes',
    'admin.cuenta': 'Cuenta',
    'admin.registrar_cobrador': 'Registrar cobrador',
}

def get_route_name(endpoint):
    """Obtiene el nombre amigable de la ruta para el encabezado del dashboard."""
    return ROUTE_NAMES.get(endpoint, 'Panel de Administración')

# -------------------------------------------------------------
# Funciones Auxiliares de Seguridad
# -------------------------------------------------------------

def check_assignment(collector_user_id, admin_user_id):
    """Verifica si el User (Collector) está asignado al User (Admin) logueado."""
    return CollectorAssignment.query.filter_by(
        admin_id=admin_user_id,
        collector_id=collector_user_id
    ).first()

# -------------------------------------------------------------
# RUTAS DE VISTA (HTML)
# -------------------------------------------------------------

@admin_bp.route('/inicio')
@login_required
def inicio():
    if not current_user.is_admin:
        return "No tienes permisos para acceder a esta página", 403
    
    return render_template('admin/inicio.html', 
                           route_name=get_route_name(request.endpoint))

@admin_bp.route('/cobradores')
@login_required
def cobradores():
    if not current_user.is_admin:
        return "No tienes permisos", 403
    
    # TAREA: Modificar queries para que admin solo vea sus relaciones
    assigned_collector_ids = db.session.query(CollectorAssignment.collector_id).filter(
        CollectorAssignment.admin_id == current_user.id
    ).subquery() 
    
    # Filtra los usuarios para mostrar solo los que tienen una asignación con el admin logueado
    usuarios = User.query.filter(User.id.in_(assigned_collector_ids)).all()
    
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
                # Asumiendo que 'rol' mapea a is_collector/is_admin en tu modelo User
                rol=form.rol.data 
            )
            # Asumiendo que user.set_password() existe o usamos la asignación directa
            user.password_hash = generate_password_hash(form.password.data)
            
            db.session.add(user)
            db.session.flush() # Obtiene el user.id antes de commit
            
            # TAREA CRUCIAL: Asignar el nuevo cobrador al admin logueado
            new_assignment = CollectorAssignment(
                admin_id=current_user.id,
                collector_id=user.id 
            )
            db.session.add(new_assignment)
            db.session.commit()
            
            flash('Cobrador registrado y asignado con éxito.', 'success')
            
            return redirect(url_for('admin.cobradores')) 
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar el usuario: {str(e)}', 'error')
    
    return render_template('admin/registrar_cobrador.html', 
                           form=form,
                           route_name=get_route_name(request.endpoint))

# -------------------------------------------------------------
# ENDPOINTS - GESTIÓN DE COBRADORES
# -------------------------------------------------------------

# ENDPOINT 1: GET /admin/collectors (API Lectura)
@admin_bp.route('/collectors', methods=['GET']) 
@login_required 
def get_collectors_api():
    if not current_user.is_admin: 
         return jsonify({"message": "Acceso no autorizado. Se requiere rol de administrador."}), 403
         
    admin_id = current_user.id
    
    assigned_collector_ids = db.session.query(CollectorAssignment.collector_id).filter(
        CollectorAssignment.admin_id == admin_id
    ).subquery() 

    all_collectors = User.query.filter(
        User.id.in_(assigned_collector_ids)
    ).all()
    
    active_collectors = []
    inactive_collectors = []
    
    for user in all_collectors:
        # Contar clientes asignados usando la relación definida
        assigned_customers_count = user.customers_as_collector.count() 
        
        collector_data = {
            "id": user.id,
            "name": user.name,
            "phone": user.phone,
            "email": user.email,
            "username": user.username,
            "assigned_customers_count": assigned_customers_count, 
            "status": user.status,
            "last_connection": user.last_connection.isoformat() if user.last_connection else None
        }

        if user.status:
            active_collectors.append(collector_data)
        else:
            inactive_collectors.append(collector_data)
            
    return jsonify({
        "active_collectors": active_collectors,
        "inactive_collectors": inactive_collectors
    }), 200

# ENDPOINT 2: POST /admin/collectors (API Creación JSON)
@admin_bp.route('/collectors', methods=['POST'])
@login_required
def add_collector_api():
    if not current_user.is_admin:
         return jsonify({"message": "Acceso no autorizado."}), 403
         
    data = request.get_json()
    
    # VALIDACIÓN DE UNICIDAD
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({"message": "El email ya está registrado."}), 400
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({"message": "El username ya está registrado."}), 400

    new_collector_user = User(
        name=data.get('name'),
        phone=data.get('phone', None), 
        email=data.get('email'),
        username=data.get('username'),
        is_collector=True, 
        is_admin=False,
        status=True,
        rol='collector' 
    )
    
    # HASH DE CONTRASEÑA
    new_collector_user.password_hash = generate_password_hash(data.get('password'))

    try:
        db.session.add(new_collector_user)
        db.session.flush() 
        
        # ASIGNACIÓN OBLIGATORIA AL CREAR
        new_assignment = CollectorAssignment(
            admin_id=current_user.id,
            collector_id=new_collector_user.id 
        )
        db.session.add(new_assignment)
        db.session.commit()
        
        return jsonify({"message": "Cobrador creado y asignado con éxito.", "id": new_collector_user.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error al crear el cobrador: {str(e)}"}), 500

# ENDPOINT 3: PUT  (Edición de Información Básica)
@admin_bp.route('/collectors/<int:id>', methods=['PUT'])
@login_required
def edit_collector_api(id):
    if not current_user.is_admin:
         return jsonify({"message": "Acceso no autorizado."}), 403
         
    # CONTROL DE SEGURIDAD: Solo editar cobradores asignados
    if not check_assignment(id, current_user.id):
        return jsonify({"message": "No tiene permiso para editar este cobrador."}), 403

    collector_user = User.query.get_or_404(id)
    data = request.get_json()
    
    collector_user.name = data.get('name', collector_user.name)
    collector_user.phone = data.get('phone', collector_user.phone)
    
    # VALIDACIÓN DE UNICIDAD de Email
    if data.get('email') and data['email'] != collector_user.email:
        if User.query.filter(User.email == data['email'], User.id != id).first():
            return jsonify({"message": "El email ya está en uso."}), 400
        collector_user.email = data['email']

    try:
        db.session.commit()
        return jsonify({"message": "Cobrador actualizado con éxito."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error al actualizar: {str(e)}"}), 500

# ENDPOINT 4: PATCH (Activar/Desactivar)
@admin_bp.route('/collectors/<int:id>/status', methods=['PATCH'])
@login_required
def toggle_collector_status_api(id):
    if not current_user.is_admin:
         return jsonify({"message": "Acceso no autorizado."}), 403
         
    # CONTROL DE SEGURIDAD: Solo cambiar estado de cobradores asignados
    if not check_assignment(id, current_user.id):
        return jsonify({"message": "No tiene permiso para cambiar el estado de este cobrador."}), 403

    collector_user = User.query.get_or_404(id)
    data = request.get_json()
    new_status = data.get('status')
    
    if new_status is None or not isinstance(new_status, bool):
        return jsonify({"message": "El campo 'status' (booleano) es requerido."}), 400
        
    collector_user.status = new_status

    try:
        db.session.commit()
        action = "activado" if new_status else "desactivado"
        return jsonify({"message": f"Cobrador {action} con éxito.", "status": new_status}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error al actualizar el estado: {str(e)}"}), 500

# ENDPOINT 5: PUT  (Actualizar credenciales)
@admin_bp.route('/collectors/<int:id>/account', methods=['PUT'])
@login_required
def update_collector_credentials_api(id):
    if not current_user.is_admin:
         return jsonify({"message": "Acceso no autorizado."}), 403
         
    # CONTROL DE SEGURIDAD: Solo modificar credenciales de cobradores asignados
    if not check_assignment(id, current_user.id):
        return jsonify({"message": "No tiene permiso para modificar las credenciales de este cobrador."}), 403

    collector_user = User.query.get_or_404(id)
    data = request.get_json()
    
    # VALIDACIÓN DE UNICIDAD de Username
    if 'username' in data and data['username'] != collector_user.username:
        if User.query.filter(User.username == data['username'], User.id != id).first():
            return jsonify({"message": "El nuevo username ya está en uso."}), 400
        collector_user.username = data['username']

    # HASH DE CONTRASEÑA
    if 'password' in data and data['password']:
        collector_user.password_hash = generate_password_hash(data['password'])

    try:
        db.session.commit()
        return jsonify({"message": "Credenciales actualizadas con éxito."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error al actualizar: {str(e)}"}), 500


# -------------------------------------------------------------
# MANEJADORES DE PETICIONES GLOBALES
# -------------------------------------------------------------

@admin_bp.after_request
def add_security_headers_admin(response):
    """
    Añade encabezados para evitar el caching de las páginas de administración.
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