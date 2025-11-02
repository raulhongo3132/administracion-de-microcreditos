from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, DateField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, Optional

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

class LoanEditForm(FlaskForm):
    collector_id = SelectField('Cobrador asignado', coerce=int, validators=[DataRequired()])
    status = SelectField('Estado', choices=[
        ('active', 'Activo'),
        ('delinquent', 'En mora'),
        ('paid', 'Pagado'),
        ('cancelled', 'Cancelado')
    ], validators=[DataRequired()])
    submit = SubmitField('Actualizar Préstamo')