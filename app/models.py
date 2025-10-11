from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    password_hash = db.Column(db.String(512), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='cliente')  # 'cliente', 'cobrador', 'admin'
    estado = db.Column(db.String(20), nullable=False, default='activo')  # 'activo', 'desactivo'

    # Propiedad para manejar el password de forma segura
    @property
    def password(self):
        raise AttributeError("El password no se puede leer directamente")

    @password.setter
    def password(self, password_plaintext):
        self.password_hash = generate_password_hash(password_plaintext)

    # Verificación de contraseña
    def check_password(self, password_plaintext):
        return check_password_hash(self.password_hash, password_plaintext)

    # Método de autenticación
    @staticmethod
    def authenticate(username, password):
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"

