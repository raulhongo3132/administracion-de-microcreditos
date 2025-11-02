from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from app.models import User

class UserRegistrationForm(FlaskForm):
    name = StringField('Nombre completo', validators=[DataRequired(), Length(max=100)])
    username = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=50)])
    phone = StringField('Teléfono', validators=[DataRequired(), Length(min=10, max=15)])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email(), Length(max=120)])
    rol = SelectField('Rol', choices=[
        ('admin', 'Administrador'), 
        ('collector', 'Cobrador')
    ], validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Registrar Usuario')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Este usuario ya está registrado.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este correo electrónico ya está registrado.')

class UserEditForm(FlaskForm):
    name = StringField('Nombre completo', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Teléfono', validators=[DataRequired(), Length(min=10, max=15)])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email(), Length(max=120)])
    status = SelectField('Estado', choices=[
        (True, 'Activo'),
        (False, 'Inactivo')
    ], coerce=bool, validators=[DataRequired()])
    submit = SubmitField('Actualizar Usuario')

class CollectorAssignmentForm(FlaskForm):
    collector_id = SelectField('Cobrador', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Asignar Cobrador')