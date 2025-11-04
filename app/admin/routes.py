from flask import Blueprint, render_template, request, after_this_request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.admin.forms import UserRegistrationForm
from app.models import User, Cliente 
from app.models import User
from werkzeug.security import generate_password_hash
from app import db

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
            
            flash('Cobrador registrado correctamente ✅', 'success')
            return redirect(url_for('admin.cobradores'))
            
        except Exception:
            db.session.rollback()
            flash('Error al registrar el usuario. Intenta nuevamente.', 'error')
    
    return render_template('admin/registrar_cobrador.html', 
                           form=form,
                           route_name=get_route_name(request.endpoint))

from app.models import User, Cliente  # asegúrate que Cliente esté importado

@admin_bp.route('/clientes_cobrador/<int:id>')
@login_required
def clientes_por_cobrador(id):
    cobrador = User.query.get_or_404(id)

    # Filtra los clientes asignados al cobrador
    clientes = Cliente.query.filter_by(cobrador_id=id).all()

    return render_template('admin/clientes.html',
                           cobrador=cobrador,
                           clientes=clientes)


@admin_bp.route('/editar_cobrador/<int:id>', methods=['POST'])
@login_required
def editar_cobrador(id):
    cobrador = User.query.get_or_404(id)
    cobrador.name = request.form['name']
    cobrador.phone = request.form['phone']
    cobrador.email = request.form['email']
    db.session.commit()
    flash('Datos del cobrador actualizados correctamente ✅', 'success')
    return redirect(url_for('admin.cobradores'))


@admin_bp.route('/editar_cuenta_cobrador/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_cuenta_cobrador(id):
    cobrador = User.query.get_or_404(id)

    if request.method == 'POST':
        cobrador.username = request.form['username']
        cobrador.email = request.form['email']
        password = request.form.get('password')
        if password:
            cobrador.password_hash = generate_password_hash(password)

        db.session.commit()
        flash('Cuenta del cobrador actualizada correctamente ✅', 'success')
        return redirect(url_for('admin.cobradores'))

    return render_template('admin/editar_cuenta_cobrador.html', cobrador=cobrador)


@admin_bp.route('/desactivar_cobrador/<int:id>', methods=['POST'])
@login_required
def desactivar_cobrador(id):
    cobrador = User.query.get_or_404(id)
    cobrador.status = not cobrador.status  # cambia entre activo/inactivo
    db.session.commit()
    estado = "activado" if cobrador.status else "desactivado"
    flash(f'Cobrador {estado} correctamente', 'info')
    return redirect(url_for('admin.cobradores'))


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
    pass
