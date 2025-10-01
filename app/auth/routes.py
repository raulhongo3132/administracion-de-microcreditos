from flask import render_template, redirect, url_for, flash, request
from app.auth import bp

@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Por ahora sin formularios, solo la página básica
    return render_template('auth/login.html', title='Iniciar Sesión')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    # Por ahora sin formularios, solo la página básica
    return render_template('auth/register.html', title='Registrarse')