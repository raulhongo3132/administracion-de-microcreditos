from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user
from urllib.parse import urlparse

from app import login_manager
from . import auth_bp
from .forms import LoginForm
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
