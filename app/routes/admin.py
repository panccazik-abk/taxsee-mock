from flask import Blueprint, jsonify, request
from app.models import db
from app.models.user import User
from app.models.shift import Shift

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/seed', methods=['POST'])
def seed_data():
    """Seed database dengan data awal"""
    if User.query.count() > 0:
        return jsonify({'status': 'already seeded'}), 200
    
    users = [
        User(username='driver1', user_id='85468140', balance=18912,
             city='Jakarta', vehicle_plate='B3475PKKK'),
        User(username='driver2', user_id='85468141', balance=50000,
             city='Jakarta', vehicle_plate='B1234XYZ'),
    ]
    db.session.add_all(users)
    
    shifts = [
        Shift(title='Program Turbo Prioritas - 3 Jam',
              sub_title='ID Maxim Jakarta',
              description='Shift pagi Jakarta Pusat',
              price=15000, duration=3, city='Jakarta'),
        Shift(title='Program Turbo Prioritas - 6 Jam',
              sub_title='ID Maxim Jakarta',
              description='Shift pagi Jakarta Selatan',
              price=25000, duration=6, city='Jakarta'),
        Shift(title='Program Turbo Malam - 3 Jam',
              sub_title='ID Maxim Jakarta',
              description='Shift malam bonus 20%',
              price=20000, duration=3, city='Jakarta'),
    ]
    db.session.add_all(shifts)
    db.session.commit()
    
    return jsonify({
        'status': 'seeded',
        'users': len(users),
        'shifts': len(shifts)
    }), 201

@admin_bp.route('/admin/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify({'users': [u.to_dict() for u in users]}), 200
