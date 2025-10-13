from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length, NumberRange

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='El email es obligatorio'),
        Email(message='Formato de email inválido')
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es obligatoria'),
        Length(min=6, message='La contraseña debe tener al menos 6 caracteres')
    ])
    submit = SubmitField('Iniciar Sesión')

class ContactoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[
        DataRequired(message='El nombre es obligatorio'),
        Length(min=2, max=50, message='El nombre debe tener entre 2 y 50 caracteres')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='El email es obligatorio'),
        Email(message='Formato de email inválido')
    ])
    edad = IntegerField('Edad', validators=[
        NumberRange(min=1, max=120, message='La edad debe estar entre 1 y 120 años')
    ])
    ciudad = SelectField('Ciudad', choices=[
        ('', 'Selecciona una ciudad'),
        ('madrid', 'Madrid'),
        ('barcelona', 'Barcelona'),
        ('valencia', 'Valencia'),
        ('sevilla', 'Sevilla'),
        ('bilbao', 'Bilbao')
    ], validators=[DataRequired(message='Selecciona una ciudad')])
    mensaje = TextAreaField('Mensaje', validators=[
        DataRequired(message='El mensaje es obligatorio'),
        Length(min=10, max=500, message='El mensaje debe tener entre 10 y 500 caracteres')
    ])
    submit = SubmitField('Enviar Mensaje')