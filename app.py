from flask import Flask, render_template, request, flash, redirect, url_for
from forms import LoginForm, ContactoForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secreta_muy_segura'  # Cambia esto por una clave real

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/usuario/<nombre>')
def usuario(nombre):
    return render_template('usuario.html', 
                         nombre=nombre, 
                         edad=25,
                         hobbies=['programar', 'leer', 'deportes'])

@app.route('/condicionales/<int:edad>')
def condicionales(edad):
    return render_template('condicionales.html', edad=edad)

# NUEVAS RUTAS PARA FORMULARIOS
@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    form = ContactoForm()
    
    if form.validate_on_submit():
        # Procesar los datos del formulario
        nombre = form.nombre.data
        email = form.email.data
        edad = form.edad.data
        ciudad = form.ciudad.data
        mensaje = form.mensaje.data
        
        # Mostrar mensaje flash
        flash(f'¡Gracias {nombre}! Tu mensaje ha sido enviado correctamente.', 'success')
        
        # Aquí normalmente guardarías en base de datos o enviarías email
        print(f"Mensaje de {nombre} ({email}, {edad} años, {ciudad}): {mensaje}")
        
        # Redirigir para evitar reenvío del formulario
        return redirect(url_for('contacto'))
    
    return render_template('contacto.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        # Aquí normalmente verificarías en la base de datos
        if email == "usuario@ejemplo.com" and password == "123456":
            flash('¡Inicio de sesión exitoso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Email o contraseña incorrectos', 'error')
    
    return render_template('login.html', form=form)

@app.route('/formulario-simple', methods=['GET', 'POST'])
def formulario_simple():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        flash(f'Formulario simple recibido: {nombre} - {email}', 'info')
        return redirect(url_for('formulario_simple'))
    
    return render_template('formulario_simple.html')

if __name__ == '__main__':
    app.run(debug=True)