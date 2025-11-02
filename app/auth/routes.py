from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime, timedelta
from app.auth import auth_bp  # Importar desde el mismo módulo
from app.models import User, RecoveryCode
from app.auth.forms import LoginForm, PasswordRecoveryForm, CodeVerificationForm, ResetPasswordForm
from app import db
import random

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Redirigir según el rol
        if current_user.is_admin:
            return redirect(url_for('admin.inicio'))
        elif current_user.is_collector:
            return redirect(url_for('collectors.inicio'))
        else:
            return redirect(url_for('customers.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data) and user.status:
            login_user(user)
            user.last_connection = datetime.utcnow()
            db.session.commit()
            
            flash(f'Bienvenido {user.name}!', 'success')
            
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            elif user.is_admin:
                return redirect(url_for('admin.inicio'))
            elif user.is_collector:
                return redirect(url_for('collectors.inicio'))
            else:
                return redirect(url_for('customers.dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/password-recovery', methods=['GET', 'POST'])
def password_recovery():
    form = PasswordRecoveryForm()
    if form.validate_on_submit():
        email = form.email.data
        
        # Buscar usuario por teléfono
        user = User.query.filter_by(email=email, status=True).first()
        
        if user:
            # Generar código de 6 dígitos
            code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            expires_at = datetime.utcnow() + timedelta(minutes=15)  # 15 minutos de validez
            
            # Crear o actualizar código de recuperación
            existing_code = RecoveryCode.query.filter_by(user_id=user.id, used=False).first()
            if existing_code:
                existing_code.code = code
                existing_code.expires_at = expires_at
                existing_code.used = False
            else:
                recovery_code = RecoveryCode(
                    user_id=user.id,
                    code=code,
                    expires_at=expires_at
                )
                db.session.add(recovery_code)
            
            db.session.commit()
            
            # ⚠️ EN PRODUCCIÓN: Aquí integrarías con un servicio SMS como Twilio
            print(f"🔐 Código de recuperación para {user.name}: {code}")
            
            flash(f'Se ha enviado un código de verificación al teléfono {email}', 'success')
            return redirect(url_for('auth.verify_code', user_id=user.id))
        else:
            flash('No se encontró una cuenta con ese correo electronico', 'error')
    
    return render_template('auth/password_recovery.html', form=form)

@auth_bp.route('/verify-code/<int:user_id>', methods=['GET', 'POST'])
def verify_code(user_id):
    form = CodeVerificationForm()
    user = User.query.get_or_404(user_id)
    
    if form.validate_on_submit():
        code = form.code.data
        
        # Buscar código válido
        recovery_code = RecoveryCode.query.filter_by(
            user_id=user_id, 
            code=code, 
            used=False
        ).first()
        
        if recovery_code and recovery_code.is_valid():
            recovery_code.used = True
            db.session.commit()
            flash('Código verificado correctamente', 'success')
            return redirect(url_for('auth.reset_password', user_id=user_id))
        else:
            flash('Código inválido o expirado', 'error')
    
    return render_template('auth/verify_code.html', form=form, user=user)

@auth_bp.route('/reset-password/<int:user_id>', methods=['GET', 'POST'])
def reset_password(user_id):
    form = ResetPasswordForm()
    user = User.query.get_or_404(user_id)
    
    if form.validate_on_submit():
        # Actualizar contraseña
        user.set_password(form.new_password.data)
        db.session.commit()
        
        flash('Contraseña restablecida correctamente. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', form=form, user=user)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('auth.login'))