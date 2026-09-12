from app.models import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    shift_id = db.Column(db.Integer, db.ForeignKey('shifts.id'))
    amount = db.Column(db.Integer)
    status = db.Column(db.String(20))
    reason = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'shift_id': self.shift_id,
            'amount': self.amount,
            'status': self.status,
            'reason': self.reason,
            'created_at': self.created_at.isoformat()
        }
