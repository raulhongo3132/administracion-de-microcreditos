from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
import re

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Iniciar sesión')

class ForgotPasswordForm(FlaskForm):
    phone = StringField('Número de teléfono', validators=[
        DataRequired(), 
        Length(min=10, max=15, message='El número debe tener entre 10 y 15 caracteres')
    ])
    submit = SubmitField('Enviar código')
    
    def validate_phone(self, field):
        # Validación básica de formato de teléfono (solo números y algunos caracteres especiales)
        phone_pattern = r'^[\+]?[\d\s\-\(\)]+$'
        if not re.match(phone_pattern, field.data):
            raise ValidationError('Por favor ingresa un número de teléfono válido')

class CodeVerificationForm(FlaskForm):
    code = StringField('Código de verificación', validators=[
        DataRequired(), 
        Length(min=4, max=6, message='El código debe tener entre 4 y 6 caracteres')
    ])
    submit = SubmitField('Verificar código')

class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('Nueva contraseña', validators=[
        DataRequired(), 
        Length(min=6, message='La contraseña debe tener al menos 6 caracteres')
    ])
    confirm_password = PasswordField('Confirmar contraseña', validators=[
        DataRequired(),
        EqualTo('new_password', message='Las contraseñas deben coincidir')
    ])
    submit = SubmitField('Actualizar contraseña')

    def validate_confirm_password(self, field):
        if self.new_password.data != field.data:
            raise ValidationError('Las contraseñas no coinciden')