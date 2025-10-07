from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)  # login
    name = db.Column(db.String(80), nullable=False)                   # nombre real
    phone = db.Column(db.String(20), unique=True, nullable=True)      # para recuperación de contraseña
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='customer')# admin / collector / customer

    def __init__(self, username, name, role, phone=None):
        self.username = username
        self.name = name
        self.role = role
        self.phone = phone

    def __repr__(self):
        return f'<User {self.username}>'

    # ========================
    # Password
    # ========================
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # ========================
    # CRUD
    # ========================
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # ========================
    # Métodos estáticos de búsqueda
    # ========================
    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_all():
        return User.query.all()
    
    @classmethod
    def get_by_phone(cls, phone):
        # Implementar la búsqueda por teléfono según tu ORM
        return cls.query.filter_by(phone=phone).first()
