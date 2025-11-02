from app import db, login_manager

# Archivo principal que establece las relaciones y importa todo
from app.models import *

# Ahora establecemos las relaciones que requieren imports cruzados

# Relaciones de User
User.collector_assignments_as_admin = db.relationship(
    'CollectorAssignment', 
    foreign_keys='CollectorAssignment.admin_id',
    backref='admin'
)
User.collector_assignments_as_collector = db.relationship(
    'CollectorAssignment',
    foreign_keys='CollectorAssignment.collector_id',
    backref='collector'
)
User.customers_as_admin = db.relationship(
    'Customer', 
    foreign_keys='Customer.admin_id', 
    backref='admin_owner'
)
User.customers_as_collector = db.relationship(
    'Customer', 
    foreign_keys='Customer.collector_id', 
    backref='assigned_collector'
)
User.loans_as_admin = db.relationship(
    'Loan', 
    foreign_keys='Loan.admin_id', 
    backref='loan_admin'
)
User.loans_as_collector = db.relationship(
    'Loan', 
    foreign_keys='Loan.collector_id', 
    backref='loan_collector'
)
User.payments_made = db.relationship(
    'Payment', 
    foreign_keys='Payment.collector_id', 
    backref='payment_collector'
)
User.penalties_applied = db.relationship(
    'LoanPenalty', 
    foreign_keys='LoanPenalty.applied_by', 
    backref='applied_by_user'
)

# Relaciones de Customer
Customer.loans = db.relationship(
    'Loan', 
    backref='customer', 
    cascade='all, delete-orphan'
)

# Relaciones de Loan
Loan.payments = db.relationship(
    'Payment', 
    backref='loan', 
    cascade='all, delete-orphan'
)
Loan.penalties = db.relationship(
    'LoanPenalty', 
    backref='loan', 
    cascade='all, delete-orphan'
)