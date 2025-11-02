from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, Optional

class CustomerRegistrationForm(FlaskForm):
    name = StringField('Nombre completo', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Teléfono', validators=[DataRequired(), Length(min=10, max=15)])
    collector_id = SelectField('Cobrador asignado', coerce=int, validators=[DataRequired()])
    notes = TextAreaField('Notas adicionales', validators=[Optional()])
    submit = SubmitField('Registrar Cliente')

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