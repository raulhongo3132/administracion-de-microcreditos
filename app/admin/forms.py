from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from app.models import User
from wtforms.validators import DataRequired, Email, Length, ValidationError, Regexp

class UserRegistrationForm(FlaskForm):
    name = StringField('Nombre completo', validators=[
        DataRequired(message='El nombre es obligatorio'),
        Length(max=100, message='El nombre no puede exceder 100 caracteres'),
        Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', 
               message='El nombre solo puede contener letras y espacios')
    ])
    
    username = StringField('Usuario', validators=[
        DataRequired(message='El usuario es obligatorio'),
        Length(min=3, max=50, message='El usuario debe tener entre 3 y 50 caracteres'),
        Regexp(r'^[a-zA-Z0-9_]+$', 
               message='El usuario solo puede contener letras, números y guiones bajos')
    ])
    
    phone = StringField('Teléfono', validators=[
        DataRequired(message='El teléfono es obligatorio'),
        Length(min=10, max=15, message='El teléfono debe tener entre 10 y 15 dígitos'),
        Regexp(r'^\+?[0-9\s\-\(\)]+$', 
               message='Formato de teléfono inválido. Use solo números, espacios y los caracteres + - ( )')
    ])
    
    email = StringField('Correo electrónico', validators=[
        DataRequired(message='El email es obligatorio'),
        Email(message='Formato de email inválido'),
        Length(max=120, message='El email no puede exceder 120 caracteres')
    ])
    
    rol = SelectField('Rol', choices=[
        ('admin', 'Administrador'), 
        ('collector', 'Cobrador')
    ], validators=[DataRequired(message='Debe seleccionar un rol')])
    
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es obligatoria'),
        Length(min=6, message='La contraseña debe tener al menos 6 caracteres'),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', 
               message='La contraseña debe contener al menos una mayúscula, una minúscula y un número')
    ])
    
    submit = SubmitField('Registrar Usuario')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Este usuario ya está registrado.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este correo electrónico ya está registrado.')



class CobradorEditForm(FlaskForm):
    name = StringField('Nombre completo', validators=[
        DataRequired(message='El nombre es obligatorio'),
        Length(max=100, message='El nombre no puede exceder 100 caracteres'),
        Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', 
               message='El nombre solo puede contener letras y espacios')
    ])
    
    phone = StringField('Teléfono', validators=[
        DataRequired(message='El teléfono es obligatorio'),
        Length(min=10, max=15, message='El teléfono debe tener entre 10 y 15 dígitos'),
        Regexp(r'^\+?[0-9\s\-\(\)]+$', 
               message='Formato de teléfono inválido. Use solo números, espacios y los caracteres + - ( )')
    ])
    
    email = StringField('Correo electrónico', validators=[
        DataRequired(message='El email es obligatorio'),
        Email(message='Formato de email inválido'),
        Length(max=120, message='El email no puede exceder 120 caracteres')
    ])
    
    submit = SubmitField('Guardar cambios')

class CuentaCobradorEditForm(FlaskForm):
    username = StringField('Usuario', validators=[
        DataRequired(message='El usuario es obligatorio'),
        Length(min=3, max=50, message='El usuario debe tener entre 3 y 50 caracteres'),
        Regexp(r'^[a-zA-Z0-9_]+$', 
               message='El usuario solo puede contener letras, números y guiones bajos')
    ])
    
    password = PasswordField('Nueva Contraseña', validators=[
        Length(min=6, message='La contraseña debe tener al menos 6 caracteres'),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', 
               message='La contraseña debe contener al menos una mayúscula, una minúscula y un número')
    ])
    
    submit = SubmitField('Actualizar cuenta')

class CollectorAssignmentForm(FlaskForm):
    collector_id = SelectField('Cobrador', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Asignar Cobrador')