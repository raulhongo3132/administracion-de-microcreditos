from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms import LoginForm, RegistroForm, ContactoForm
from models import Usuario, MensajeContacto, crear_datos_ejemplo
from database import db, init_app

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secreta_muy_segura'

# Configuración de la base de datos
init_app(app)

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Crear datos de ejemplo al iniciar (solo en desarrollo)
with app.app_context():
    crear_datos_ejemplo()

# Rutas públicas
@app.route('/')
def index():
    # Contar usuarios y mensajes para mostrar en la página principal
    total_usuarios = Usuario.query.count()
    total_mensajes = MensajeContacto.query.count()
    
    return render_template('index.html', 
                         total_usuarios=total_usuarios,
                         total_mensajes=total_mensajes)

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
        
        # Guardar en base de datos
        nuevo_mensaje = MensajeContacto(
            nombre=nombre,
            email=email,
            edad=edad,
            ciudad=ciudad,
            mensaje=mensaje,
            usuario_id=current_user.id if current_user.is_authenticated else None
        )
        
        db.session.add(nuevo_mensaje)
        db.session.commit()
        
        flash(f'¡Gracias {nombre}! Tu mensaje ha sido enviado correctamente.', 'success')
        return redirect(url_for('contacto'))
    
    return render_template('contacto.html', form=form)

# Rutas de autenticación
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember_me = form.remember_me.data
        
        # Buscar usuario en la base de datos
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and usuario.check_password(password):
            if usuario.activo:
                login_user(usuario, remember=remember_me)
                flash(f'¡Bienvenido de nuevo, {usuario.nombre}!', 'success')
                
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            else:
                flash('Tu cuenta está desactivada.', 'error')
        else:
            flash('Email o contraseña incorrectos', 'error')
    
    return render_template('login.html', form=form)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistroForm()
    
    if form.validate_on_submit():
        nombre = form.nombre.data
        email = form.email.data
        password = form.password.data
        
        # Crear nuevo usuario
        nuevo_usuario = Usuario(nombre=nombre, email=email)
        nuevo_usuario.set_password(password)
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
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
    # Obtener estadísticas del usuario
    mensajes_usuario = MensajeContacto.query.filter_by(usuario_id=current_user.id).count()
    
    return render_template('dashboard.html', 
                         mensajes_usuario=mensajes_usuario)

@app.route('/perfil')
@login_required
def perfil():
    # Obtener los mensajes del usuario
    mensajes = MensajeContacto.query.filter_by(usuario_id=current_user.id).order_by(
        MensajeContacto.fecha_creacion.desc()
    ).all()
    
    return render_template('perfil.html', mensajes=mensajes)

@app.route('/usuarios')
@login_required
def lista_usuarios():
    # Solo administradores deberían ver esto (aquí todos los usuarios logueados pueden ver)
    usuarios = Usuario.query.order_by(Usuario.fecha_creacion.desc()).all()
    return render_template('lista_usuarios.html', usuarios=usuarios)

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