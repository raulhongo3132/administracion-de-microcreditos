from flask import render_template, redirect, url_for, request, flash, session
from flask_login import current_user, login_user, logout_user
from urllib.parse import urlparse
import secrets
import string

from app import login_manager
from . import auth_bp
from .forms import LoginForm, ForgotPasswordForm, CodeVerificationForm, ResetPasswordForm
from .models import User


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Redirige según rol
        return redirect(get_dashboard_for_user(current_user))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)

            
            # Redirección segura a next si viene de una ruta protegida
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = get_dashboard_for_user(user)
            
            return redirect(next_page)
        else:
            flash('Usuario o contraseña incorrectos', 'danger')

    return render_template('auth/login_form.html', form=form)

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Paso 1: Solicitar código de verificación por SMS"""
    if current_user.is_authenticated:
        return redirect(get_dashboard_for_user(current_user))

    form = ForgotPasswordForm()
    if form.validate_on_submit():
        phone = form.phone.data
        
        # Aquí buscarías en tu base de datos si existe un usuario con ese teléfono
        # Por ahora simulamos que siempre existe para la demo
        user_exists = True  # Cambiar por: User.get_by_phone(phone) is not None
        
        if user_exists:
            # Guardar teléfono en sesión para los próximos pasos
            session['reset_phone'] = phone
            session['reset_code'] = '1234'  # Código hardcodeado por ahora
            
            # Aquí iría la lógica real para enviar SMS
            # send_sms_code(phone, session['reset_code'])
            
            flash(f'Se ha enviado un código de verificación al número {phone}.', 'info')
            return redirect(url_for('auth.verify_code'))
        else:
            flash('No existe una cuenta asociada a este número de teléfono.', 'danger')
    
    return render_template('auth/forgot_password.html', form=form)

@auth_bp.route('/verify-code', methods=['GET', 'POST'])
def verify_code():
    """Paso 2: Verificar código SMS"""
    if current_user.is_authenticated:
        return redirect(get_dashboard_for_user(current_user))
    
    # Verificar que viene del paso anterior
    if 'reset_phone' not in session:
        flash('Por favor, solicita un código de verificación primero.', 'warning')
        return redirect(url_for('auth.forgot_password'))

    form = CodeVerificationForm()
    if form.validate_on_submit():
        entered_code = form.code.data
        
        # Verificar código (hardcodeado como '1234')
        if entered_code == session.get('reset_code'):
            flash('Código verificado correctamente.', 'success')
            return redirect(url_for('auth.reset_password'))
        else:
            flash('Código incorrecto. Intenta nuevamente.', 'danger')
    
    return render_template('auth/verify_code.html', form=form)

@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    """Paso 3: Cambiar contraseña"""
    if current_user.is_authenticated:
        return redirect(get_dashboard_for_user(current_user))
    
    # Verificar que pasó por la verificación
    if 'reset_phone' not in session:
        flash('Por favor, completa la verificación primero.', 'warning')
        return redirect(url_for('auth.forgot_password'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        # Aquí buscarías al usuario por el teléfono
        phone = session['reset_phone']
        # user = User.get_by_phone(phone)
        
        # Por ahora simulamos la actualización
        # if user:
        #     user.set_password(form.new_password.data)
        #     db.session.commit()
            
        # Limpiar sesión
        session.pop('reset_phone', None)
        session.pop('reset_code', None)
        
        flash('Contraseña actualizada correctamente. Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', form=form)

@auth_bp.route('/cancel-reset')
def cancel_reset():
    """Cancelar el proceso de recuperación"""
    session.pop('reset_phone', None)
    session.pop('reset_code', None)
    flash('Proceso de recuperación cancelado.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))  # vuelve al login


@login_manager.user_loader
def load_user(user_id):
    """Carga el usuario para Flask-Login"""
    return User.get_by_id(int(user_id))


# ========================
# Función auxiliar
# ========================
def get_dashboard_for_user(user):
    """Devuelve la ruta de inicio según rol"""
    if user.role == 'admin':
        return url_for('admin.index')
    elif user.role == 'collector':
        return url_for('collectors.index')
    elif user.role == 'customer':
        return url_for('customers.index')
    else:
        # Por defecto, login
        return url_for('auth.login')
