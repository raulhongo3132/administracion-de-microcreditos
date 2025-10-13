from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from datetime import datetime

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    
    # Relación con mensajes de contacto
    mensajes = db.relationship('MensajeContacto', backref='autor', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Usuario {self.email}>'

class MensajeContacto(db.Model):
    __tablename__ = 'mensajes_contacto'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    edad = db.Column(db.Integer)
    ciudad = db.Column(db.String(50))
    mensaje = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    
    def __repr__(self):
        return f'<MensajeContacto {self.id} - {self.email}>'

# Función para crear datos de ejemplo
def crear_datos_ejemplo():
    from database import db
    
    # Verificar si ya existen usuarios
    if Usuario.query.count() == 0:
        print("Creando usuarios de ejemplo...")
        
        usuarios_ejemplo = [
            {
                'nombre': 'Ana García',
                'email': 'ana@ejemplo.com', 
                'password': 'password123'
            },
            {
                'nombre': 'Carlos López',
                'email': 'carlos@ejemplo.com',
                'password': 'password123'
            },
            {
                'nombre': 'María Rodríguez', 
                'email': 'maria@ejemplo.com',
                'password': 'password123'
            }
        ]
        
        for usuario_data in usuarios_ejemplo:
            usuario = Usuario(
                nombre=usuario_data['nombre'],
                email=usuario_data['email']
            )
            usuario.set_password(usuario_data['password'])
            db.session.add(usuario)
        
        db.session.commit()
        print("Usuarios de ejemplo creados exitosamente!")