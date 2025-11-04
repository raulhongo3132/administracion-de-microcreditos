from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo, Regexp
from app.models import User
import re

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[
        DataRequired(message='El usuario es obligatorio'),
        Regexp(r'^[a-zA-Z0-9_]{3,50}$', 
               message='El usuario debe tener entre 3 y 50 caracteres y solo puede contener letras, números y guiones bajos')
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es obligatoria'),
        Length(min=1, message='La contraseña es obligatoria')  # Mínimo 1 carácter para evitar espacios en blanco
    ])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')

class PasswordRecoveryForm(FlaskForm):
    email = StringField('Correo electrónico', validators=[
        DataRequired(message='El email es obligatorio'),
        Email(message='Formato de email inválido'),
        Regexp(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
               message='Formato de email inválido. Ejemplo: usuario@dominio.com')
    ])
    submit = SubmitField('Enviar Código')

class CodeVerificationForm(FlaskForm):
    code = StringField('Código de verificación', validators=[
        DataRequired(message='El código es obligatorio'),
        Length(min=6, max=6, message='El código debe tener exactamente 6 caracteres'),
        Regexp(r'^[A-Z0-9]{6}$',
               message='El código debe contener solo letras mayúsculas y números (6 caracteres)')
    ])
    submit = SubmitField('Verificar Código')

class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('Nueva Contraseña', validators=[
        DataRequired(message='La nueva contraseña es obligatoria'),
        Length(min=6, message='La contraseña debe tener al menos 6 caracteres'),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]',
               message='La contraseña debe contener al menos una mayúscula, una minúscula, un número y un carácter especial (@$!%*?&)')
    ])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(message='Debe confirmar la contraseña'),
        EqualTo('new_password', message='Las contraseñas deben coincidir')
    ])
    submit = SubmitField('Restablecer Contraseña')