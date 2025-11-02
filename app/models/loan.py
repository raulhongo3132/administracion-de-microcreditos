from datetime import datetime, timedelta
from app import db

class Loan(db.Model):
    __tablename__ = 'loans'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    collector_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Datos del préstamo
    amount_delivered = db.Column(db.Numeric(10, 2), nullable=False)
    interest_rate = db.Column(db.Numeric(5, 4), nullable=False)
    term_days = db.Column(db.Integer, nullable=False)
    daily_payment = db.Column(db.Numeric(10, 2), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    current_balance = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Fechas
    start_date = db.Column(db.DateTime, nullable=False)
    expected_end_date = db.Column(db.DateTime, nullable=False)
    actual_end_date = db.Column(db.DateTime)
    
    # Estado
    status = db.Column(db.String(20), default='active')
    days_paid = db.Column(db.Integer, default=0)
    total_days_paid = db.Column(db.Integer, default=0)
    
    # Relaciones (se definirán en el archivo principal)
    
    def calculate_totals(self):
        """Calcula los totales cuando se crea el préstamo"""
        self.total_amount = self.amount_delivered * (1 + self.interest_rate)
        self.daily_payment = self.total_amount / self.term_days
        self.current_balance = self.total_amount
        self.expected_end_date = self.start_date + timedelta(days=self.term_days)
    
    def add_payment(self, amount, days_covered, collector_id, notes=None):
        """Agrega un pago al préstamo"""
        from app.models import Payment  # Import aquí para evitar circular
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

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loans.id'), nullable=False)
    collector_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    days_covered = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Payment {self.id} - Loan:{self.loan_id} - Amount:{self.amount}>'

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