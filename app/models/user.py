from app.models import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    user_id = db.Column(db.String(20), unique=True, nullable=False)
    balance = db.Column(db.Integer, default=0)
    city = db.Column(db.String(50))
    vehicle_plate = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    transactions = db.relationship('Transaction', backref='user', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'balance': self.balance,
            'balance_text': f"Rp {self.balance:,}".replace(",", "."),
            'city': self.city,
            'vehicle_plate': self.vehicle_plate
        }
