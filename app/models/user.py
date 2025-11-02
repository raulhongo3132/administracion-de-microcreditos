from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    rol = db.Column(db.String(20), nullable=False)  # admin/collector
    password_hash = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Boolean, default=True)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_connection = db.Column(db.DateTime)
    
    # Relaciones (se definirán en el archivo principal para evitar imports circulares)
    
    # Métodos para contraseña
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # Propiedades para fácil acceso
    @property
    def is_admin(self):
        return self.rol == 'admin'
    
    @property
    def is_collector(self):
        return self.rol == 'collector'
    
    def __repr__(self):
        return f'<User {self.username} - {self.rol}>'

class RecoveryCode(db.Model):
    __tablename__ = 'recovery_codes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    code = db.Column(db.String(6), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='recovery_codes')
    
    def is_valid(self):
        from datetime import datetime
        return not self.used and datetime.utcnow() < self.expires_at
    
    def __repr__(self):
        return f'<RecoveryCode {self.code} - User:{self.user_id}>'