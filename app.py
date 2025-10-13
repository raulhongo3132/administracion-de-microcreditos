from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms import LoginForm, RegistroForm, ContactoForm
from models import Usuario, get_user, get_user_by_email, usuarios_db
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secreta_muy_segura'

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return get_user(int(user_id))

# Rutas públicas
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

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    form = ContactoForm()
    
    if form.validate_on_submit():
        nombre = form.nombre.data
        email = form.email.data
        edad = form.edad.data
        ciudad = form.ciudad.data
        mensaje = form.mensaje.data
        
        flash(f'¡Gracias {nombre}! Tu mensaje ha sido enviado correctamente.', 'success')
        print(f"Mensaje de {nombre} ({email}, {edad} años, {ciudad}): {mensaje}")
        return redirect(url_for('contacto'))
    
    return render_template('contacto.html', form=form)

# Rutas de autenticación
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Si el usuario ya está autenticado, redirigir al dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember_me = form.remember_me.data
        
        # Buscar usuario en la "base de datos"
        usuario = get_user_by_email(email)
        
        if usuario and usuario.check_password(password):
            login_user(usuario, remember=remember_me)
            flash(f'¡Bienvenido de nuevo, {usuario.nombre}!', 'success')
            
            # Redirigir a la página que intentaba acceder o al dashboard
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Email o contraseña incorrectos', 'error')
    
    return render_template('login.html', form=form)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    # Si el usuario ya está autenticado, redirigir al dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistroForm()
    
    if form.validate_on_submit():
        nombre = form.nombre.data
        email = form.email.data
        password = form.password.data
        
        # Crear nuevo usuario
        nuevo_id = max(usuarios_db.keys()) + 1 if usuarios_db else 1
        nuevo_usuario = Usuario(nuevo_id, nombre, email, password)
        usuarios_db[nuevo_usuario.id] = nuevo_usuario
        
        # Iniciar sesión automáticamente
        login_user(nuevo_usuario)
        flash(f'¡Cuenta creada exitosamente! Bienvenido, {nombre}!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('registro.html', form=form)

@app.route('/logout')
@login_required
def logout():
    nombre_usuario = current_user.nombre
    logout_user()
    flash(f'Has cerrado sesión. ¡Hasta pronto, {nombre_usuario}!', 'info')
    return redirect(url_for('index'))

# Rutas protegidas
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html')

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