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
    email = db.Column(db.String(120), unique=True, nullable=False)  # Nuevo campo
    rol = db.Column(db.String(20), nullable=False)  # admin/collector
    password_hash = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Boolean, default=True)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_connection = db.Column(db.DateTime)
    
    # Relaciones
    collector_assignments_as_admin = db.relationship('CollectorAssignment', 
                                                   foreign_keys='CollectorAssignment.admin_id',
                                                   backref='admin')
    collector_assignments_as_collector = db.relationship('CollectorAssignment',
                                                       foreign_keys='CollectorAssignment.collector_id',
                                                       backref='collector')
    customers_as_admin = db.relationship('Customer', foreign_keys='Customer.admin_id', backref='admin_owner')
    customers_as_collector = db.relationship('Customer', foreign_keys='Customer.collector_id', backref='assigned_collector')
    loans_as_admin = db.relationship('Loan', foreign_keys='Loan.admin_id', backref='loan_admin')
    loans_as_collector = db.relationship('Loan', foreign_keys='Loan.collector_id', backref='loan_collector')
    payments_made = db.relationship('Payment', foreign_keys='Payment.collector_id', backref='payment_collector')
    penalties_applied = db.relationship('LoanPenalty', foreign_keys='LoanPenalty.applied_by', backref='applied_by_user')
    
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

class CollectorAssignment(db.Model):
    __tablename__ = 'collector_assignments'
    
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    collector_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assignment_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<CollectorAssignment Admin:{self.admin_id} -> Collector:{self.collector_id}>'

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    collector_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    status = db.Column(db.Boolean, default=True)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    
    # Relaciones
    loans = db.relationship('Loan', backref='customer', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Customer {self.name} - Collector:{self.collector_id}>'

class Loan(db.Model):
    __tablename__ = 'loans'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    collector_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Datos del préstamo
    amount_delivered = db.Column(db.Numeric(10, 2), nullable=False)
    interest_rate = db.Column(db.Numeric(5, 4), nullable=False)  # Cambiado de 'interest'
    term_days = db.Column(db.Integer, nullable=False)
    daily_payment = db.Column(db.Numeric(10, 2), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)  # Cambiado de 'original_total'
    current_balance = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Fechas
    start_date = db.Column(db.DateTime, nullable=False)
    expected_end_date = db.Column(db.DateTime, nullable=False)  # Cambiado de 'original_end_date'
    actual_end_date = db.Column(db.DateTime)  # Nuevo campo
    
    # Estado
    status = db.Column(db.String(20), default='active')  # Cambiado de 'state'
    days_paid = db.Column(db.Integer, default=0)
    total_days_paid = db.Column(db.Integer, default=0)  # Nuevo campo
    
    # Relaciones
    payments = db.relationship('Payment', backref='loan', cascade='all, delete-orphan')
    penalties = db.relationship('LoanPenalty', backref='loan', cascade='all, delete-orphan')
    
    def calculate_totals(self):
        """Calcula los totales cuando se crea el préstamo"""
        self.total_amount = self.amount_delivered * (1 + self.interest_rate)
        self.daily_payment = self.total_amount / self.term_days
        self.current_balance = self.total_amount
        
        self.expected_end_date = self.start_date + timedelta(days=self.term_days)
    
    def add_payment(self, amount, days_covered, collector_id, notes=None):
        """Agrega un pago al préstamo"""
        payment = Payment(
            loan_id=self.id,
            collector_id=collector_id,
            amount=amount,
            days_covered=days_covered,
            notes=notes
        )
        db.session.add(payment)
        
        # Actualizar balances
        self.current_balance -= amount
        self.days_paid += days_covered
        self.total_days_paid += days_covered
        
        # Verificar si el préstamo está pagado
        if self.current_balance <= 0:
            self.status = 'paid'
            self.actual_end_date = datetime.utcnow()
    
    def __repr__(self):
        return f'<Loan {self.id} - Customer:{self.customer_id} - Balance:{self.current_balance}>'

class LoanPenalty(db.Model):
    __tablename__ = 'loan_penalties'
    
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loans.id'), nullable=False)
    extra_days = db.Column(db.Integer, nullable=False)
    extra_interest_rate = db.Column(db.Numeric(5, 4), nullable=False)
    penalty_amount = db.Column(db.Numeric(10, 2), nullable=False)
    reason = db.Column(db.Text)
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)
    applied_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def apply_penalty(self):
        """Aplica la penalización al préstamo"""
        loan = Loan.query.get(self.loan_id)
        if loan:
            loan.current_balance += self.penalty_amount
            loan.total_amount += self.penalty_amount
            loan.expected_end_date += timedelta(days=self.extra_days)
            loan.status = 'delinquent'
    
    def __repr__(self):
        return f'<LoanPenalty {self.id} - Loan:{self.loan_id} - Amount:{self.penalty_amount}>'

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loans.id'), nullable=False)
    collector_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)  # Cambiado de 'monto_pagado'
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)  # Cambiado de 'fecha_pago'
    days_covered = db.Column(db.Integer, nullable=False)  # Nuevo campo
    notes = db.Column(db.Text)  # Cambiado de 'observaciones'
    
    def __repr__(self):
        return f'<Payment {self.id} - Loan:{self.loan_id} - Amount:{self.amount}>'

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
    
    def __repr__(self):
        return f'<RecoveryCode {self.code} - User:{self.user_id}>'

# Configuración de Flask-Login
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))