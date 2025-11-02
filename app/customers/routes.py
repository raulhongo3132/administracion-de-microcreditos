from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app import db
from app.customers import customers_bp
from app.customers.forms import CustomerRegistrationForm, CustomerEditForm
from app.models import Customer, User

ROUTE_NAMES = {
    'customers.index': 'Lista de Clientes',
    'customers.create': 'Registrar Cliente',
    'customers.edit': 'Editar Cliente',
}

def get_route_name(endpoint):
    return ROUTE_NAMES.get(endpoint, 'Gestión de Clientes')

@customers_bp.route('/')
@login_required
def index():
    if current_user.is_admin:
        customers = Customer.query.filter_by(admin_id=current_user.id).all()
    elif current_user.is_collector:
        customers = Customer.query.filter_by(collector_id=current_user.id).all()
    else:
        return "No tienes permisos", 403
    
    return render_template('customers/index.html', 
                         customers=customers,
                         route_name=get_route_name(request.endpoint))

@customers_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if not current_user.is_admin:
        return "No tienes permisos", 403
    
    form = CustomerRegistrationForm()
    
    # Llenar choices de cobradores
    if current_user.is_admin:
        form.collector_id.choices = [(c.id, c.name) for c in User.query.filter_by(rol='collector', status=True).all()]
    
    if form.validate_on_submit():
        customer = Customer(
            admin_id=current_user.id,
            collector_id=form.collector_id.data,
            name=form.name.data,
            phone=form.phone.data,
            notes=form.notes.data
        )
        db.session.add(customer)
        db.session.commit()
        flash('Cliente registrado exitosamente', 'success')
        return redirect(url_for('customers.index'))
    
    return render_template('customers/create.html', 
                         form=form,
                         route_name=get_route_name(request.endpoint))
