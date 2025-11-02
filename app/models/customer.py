from datetime import datetime
from app import db

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
    
    # Relaciones (se definirán en el archivo principal)
    
    def __repr__(self):
        return f'<Customer {self.name} - Collector:{self.collector_id}>'