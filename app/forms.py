from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DecimalField, TextAreaField, DateField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, Length, NumberRange, ValidationError, EqualTo, Optional
from app.models import User, Customer

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')

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

class CustomerRegistrationForm(FlaskForm):
    name = StringField('Nombre completo', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Teléfono', validators=[DataRequired(), Length(min=10, max=15)])
    collector_id = SelectField('Cobrador asignado', coerce=int, validators=[DataRequired()])
    notes = TextAreaField('Notas adicionales', validators=[Optional()])
    submit = SubmitField('Registrar Cliente')

class CollectorAssignmentForm(FlaskForm):
    collector_id = SelectField('Cobrador', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Asignar Cobrador')

class LoanForm(FlaskForm):
    customer_id = SelectField('Cliente', coerce=int, validators=[DataRequired()])
    collector_id = SelectField('Cobrador asignado', coerce=int, validators=[DataRequired()])
    amount_delivered = DecimalField('Monto entregado', validators=[DataRequired(), NumberRange(min=0.01)])
    interest_rate = DecimalField('Tasa de interés', validators=[DataRequired(), NumberRange(min=0.01, max=1)])
    term_days = SelectField('Plazo en días', choices=[
        (15, '15 días'),
        (20, '20 días'),
        (30, '30 días'),
        (40, '40 días'),
        (60, '60 días')
    ], coerce=int, validators=[DataRequired()])
    start_date = DateField('Fecha de inicio', validators=[DataRequired()])
    submit = SubmitField('Crear Préstamo')

class PaymentForm(FlaskForm):
    amount = DecimalField('Monto del pago', validators=[DataRequired(), NumberRange(min=0.01)])
    days_covered = IntegerField('Días cubiertos', validators=[DataRequired(), NumberRange(min=1)])
    notes = TextAreaField('Observaciones', validators=[Optional()])
    submit = SubmitField('Registrar Pago')

class LoanPenaltyForm(FlaskForm):
    extra_days = IntegerField('Días extra de mora', validators=[DataRequired(), NumberRange(min=1)])
    extra_interest_rate = DecimalField('Tasa de interés extra', validators=[DataRequired(), NumberRange(min=0.01, max=1)])
    reason = TextAreaField('Razón de la mora', validators=[DataRequired()])
    submit = SubmitField('Aplicar Mora')

class PasswordRecoveryForm(FlaskForm):
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    submit = SubmitField('Enviar Código')

class CodeVerificationForm(FlaskForm):
    code = StringField('Código de verificación', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('Verificar Código')

class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('Nueva Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('new_password', message='Las contraseñas deben coincidir')])
    submit = SubmitField('Restablecer Contraseña')

class CustomerEditForm(FlaskForm):
    name = StringField('Nombre completo', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Teléfono', validators=[DataRequired(), Length(min=10, max=15)])
    collector_id = SelectField('Cobrador asignado', coerce=int, validators=[DataRequired()])
    status = SelectField('Estado', choices=[
        (True, 'Activo'),
        (False, 'Inactivo')
    ], coerce=bool, validators=[DataRequired()])
    notes = TextAreaField('Notas adicionales', validators=[Optional()])
    submit = SubmitField('Actualizar Cliente')

class UserEditForm(FlaskForm):
    name = StringField('Nombre completo', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Teléfono', validators=[DataRequired(), Length(min=10, max=15)])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email(), Length(max=120)])
    status = SelectField('Estado', choices=[
        (True, 'Activo'),
        (False, 'Inactivo')
    ], coerce=bool, validators=[DataRequired()])
    submit = SubmitField('Actualizar Usuario')

class LoanEditForm(FlaskForm):
    collector_id = SelectField('Cobrador asignado', coerce=int, validators=[DataRequired()])
    status = SelectField('Estado', choices=[
        ('active', 'Activo'),
        ('delinquent', 'En mora'),
        ('paid', 'Pagado'),
        ('cancelled', 'Cancelado')
    ], validators=[DataRequired()])
    submit = SubmitField('Actualizar Préstamo')