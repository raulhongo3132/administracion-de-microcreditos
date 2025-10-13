from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DecimalField, TextAreaField, DateField, BooleanField
from wtforms.validators import DataRequired, Email, Length, NumberRange, ValidationError, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')

class UserRegistrationForm(FlaskForm):
    name = StringField('Nombre completo', validators=[DataRequired(), Length(max=100)])
    username = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=50)])
    phone = StringField('Teléfono', validators=[DataRequired(), Length(min=10, max=15)])
    rol = SelectField('Rol', choices=[
        ('customer', 'Cliente'), 
        ('collector', 'Cobrador')
    ], validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Registrar Usuario')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Este usuario ya está registrado.')

class LoanForm(FlaskForm):
    customer_id = SelectField('Cliente', coerce=int, validators=[DataRequired()])
    collector_id = SelectField('Cobrador', coerce=int, validators=[DataRequired()])
    amount_delivered = DecimalField('Monto entregado', validators=[DataRequired(), NumberRange(min=0.01)])
    interest = DecimalField('Tasa de interés', validators=[DataRequired(), NumberRange(min=0.01, max=1)])
    term_days = SelectField('Plazo en días', choices=[
        (20, '20 días'),
        (30, '30 días'),
        (40, '40 días')
    ], coerce=int, validators=[DataRequired()])
    start_date = DateField('Fecha de inicio', validators=[DataRequired()])
    submit = SubmitField('Crear Préstamo')

class PasswordRecoveryForm(FlaskForm):
    phone = StringField('Teléfono', validators=[DataRequired(), Length(min=10, max=15)])
    submit = SubmitField('Enviar Código')

class CodeVerificationForm(FlaskForm):
    code = StringField('Código de verificación', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('Verificar Código')

class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('Nueva Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('new_password', message='Las contraseñas deben coincidir')])
    submit = SubmitField('Restablecer Contraseña')