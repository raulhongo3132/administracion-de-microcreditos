# Este archivo importa todos los modelos para facilitar el acceso
from app.models.user import User, RecoveryCode
from app.models.customer import Customer, CollectorAssignment
from app.models.loan import Loan, Payment, LoanPenalty

__all__ = [
    'User',
    'RecoveryCode',
    'Customer', 
    'CollectorAssignment',
    'Loan',
    'Payment',
    'LoanPenalty'
]