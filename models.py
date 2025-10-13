from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Base de datos simulada (en producción usarías una base de datos real)
usuarios_db = {}

class Usuario(UserMixin):
    def __init__(self, id, nombre, email, password):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = generate_password_hash(password)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<Usuario {self.email}>'

# Función para obtener usuario por ID (necesaria para flask-login)
def get_user(user_id):
    return usuarios_db.get(int(user_id))

# Función para obtener usuario por email
def get_user_by_email(email):
    for user in usuarios_db.values():
        if user.email == email:
            return user
    return None

# Crear algunos usuarios de ejemplo
def crear_usuarios_ejemplo():
    if not usuarios_db:
        usuario1 = Usuario(1, "Ana García", "ana@ejemplo.com", "password123")
        usuario2 = Usuario(2, "Carlos López", "carlos@ejemplo.com", "password123")
        usuario3 = Usuario(3, "María Rodríguez", "maria@ejemplo.com", "password123")
        
        usuarios_db[usuario1.id] = usuario1
        usuarios_db[usuario2.id] = usuario2
        usuarios_db[usuario3.id] = usuario3

# Llamar a la función para crear usuarios de ejemplo
crear_usuarios_ejemplo()