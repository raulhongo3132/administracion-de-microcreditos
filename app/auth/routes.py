from flask import render_template, redirect, url_for, flash, request, current_app
from app.auth import bp

@bp.route('/login', methods=['GET', 'POST'])
def login():
    current_app.logger.info('Página de login accedida')
    return render_template('login.html', title='Iniciar Sesión')  # ← nombre simple

@bp.route('/register', methods=['GET', 'POST'])
def register():
    current_app.logger.info('Página de registro accedida')
    return render_template('register.html', title='Registrarse')  # ← nombre simple