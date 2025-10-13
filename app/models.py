from datetime import datetime, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    rol = db.Column(db.String(20), nullable=False)  # admin/collector/customer
    password_hash = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Boolean, default=True)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_connection = db.Column(db.DateTime)
    
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
    
    @property
    def is_customer(self):
        return self.rol == 'customer'
    
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
        return not self.used and datetime.utcnow() < self.expires_at

class Loan(db.Model):
    __tablename__ = 'loans'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    collector_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Datos del préstamo
    amount_delivered = db.Column(db.Numeric(10, 2), nullable=False)
    interest = db.Column(db.Numeric(5, 4), nullable=False)
    term_days = db.Column(db.Integer, nullable=False)
    daily_payment = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Moras manuales
    extra_days = db.Column(db.Integer, default=0)
    
    # Cálculos
    original_total = db.Column(db.Numeric(10, 2), nullable=False)
    current_total = db.Column(db.Numeric(10, 2), nullable=False)
    current_balance = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Fechas
    start_date = db.Column(db.DateTime, nullable=False)
    original_end_date = db.Column(db.DateTime, nullable=False)
    current_end_date = db.Column(db.DateTime, nullable=False)
    
    # Estado
    state = db.Column(db.String(20), default='activo')
    days_paid = db.Column(db.Integer, default=0)
    
    # Relaciones
    customer = db.relationship('User', foreign_keys=[customer_id], backref='loans_as_customer')
    collector = db.relationship('User', foreign_keys=[collector_id], backref='loans_as_collector')
    payments = db.relationship('Payment', backref='loan', cascade='all, delete-orphan')
    
    def calculate_totals(self):
        """Calcula los totales cuando se crea el préstamo"""
        self.original_total = self.amount_delivered * (1 + self.interest)
        self.daily_payment = self.original_total / self.term_days
        self.current_total = self.original_total
        self.current_balance = self.original_total
        
        self.original_end_date = self.start_date + timedelta(days=self.term_days)
        self.current_end_date = self.original_end_date
    
    def add_extra_days(self, days_to_add=1, extra_interest=0.05):
        """Agrega días de mora manualmente"""
        self.extra_days += days_to_add
        daily_extra = self.daily_payment * extra_interest
        total_extra = daily_extra * days_to_add
        
        self.current_total += total_extra
        self.current_balance += total_extra
        self.current_end_date += timedelta(days=days_to_add)
        
        if self.extra_days > 0:
            self.state = 'moroso'

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loans.id'), nullable=False)
    collector_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fecha_pago = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    monto_pagado = db.Column(db.Numeric(10, 2), nullable=False)
    observaciones = db.Column(db.Text)
    
    collector = db.relationship('User', foreign_keys=[collector_id], backref='payments_made')