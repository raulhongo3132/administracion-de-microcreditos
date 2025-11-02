from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, TextAreaField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, NumberRange, Optional, Length
from app.models import Customer, Loan

class CollectorPaymentForm(FlaskForm):
    amount = DecimalField('Monto del pago', validators=[DataRequired(), NumberRange(min=0.01)])
    days_covered = IntegerField('Días cubiertos', validators=[DataRequired(), NumberRange(min=1)])
    notes = TextAreaField('Observaciones', validators=[Optional()])
    submit = SubmitField('Registrar Pago')

class CollectorLoanForm(FlaskForm):
    customer_id = SelectField('Cliente', coerce=int, validators=[DataRequired()])
    amount_delivered = DecimalField('Monto entregado', validators=[DataRequired(), NumberRange(min=0.01)])
    interest_rate = DecimalField('Tasa de interés', validators=[DataRequired(), NumberRange(min=0.01, max=1)])
    term_days = SelectField('Plazo en días', choices=[
        (15, '15 días'),
        (20, '20 días'),
        (30, '30 días'),
        (40, '40 días')
    ], coerce=int, validators=[DataRequired()])
    start_date = DateField('Fecha de inicio', validators=[DataRequired()])
    submit = SubmitField('Crear Préstamo')

class CollectorCustomerForm(FlaskForm):
    name = StringField('Nombre completo', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Teléfono', validators=[DataRequired(), Length(min=10, max=15)])
    notes = TextAreaField('Notas adicionales', validators=[Optional()])
    submit = SubmitField('Registrar Cliente')