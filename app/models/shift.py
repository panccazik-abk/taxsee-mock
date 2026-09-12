from app.models import db
from datetime import datetime

class Shift(db.Model):
    __tablename__ = 'shifts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    sub_title = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, default=3)
    city = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'subTitle': self.sub_title,
            'description': self.description,
            'price': f"Rp {self.price:,}".replace(",", "."),
            'price_raw': self.price,
            'duration': self.duration,
            'city': self.city
        }
