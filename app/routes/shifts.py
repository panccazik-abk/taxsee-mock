from flask import Blueprint, jsonify, request
from app.models import db
from app.models.user import User
from app.models.shift import Shift
from app.models.transaction import Transaction
from app.middleware.auth import require_auth
from app.middleware.rate_limit import rate_limit

shifts_bp = Blueprint('shifts', __name__)

@shifts_bp.route('/api/v1/shifts', methods=['GET'])
@require_auth
def get_shifts():
    shifts = Shift.query.all()
    groups = {}
    for s in shifts:
        city = s.city or 'Lainnya'
        if city not in groups:
            groups[city] = []
        groups[city].append(s.to_dict())
    result = [{'name': k, 'shifts': v} for k, v in groups.items()]
    return jsonify({'groups': result}), 200

@shifts_bp.route('/api/v1/shift/<int:sid>/buy', methods=['POST'])
@require_auth
@rate_limit
def buy_shift(sid):
    shift = Shift.query.get(sid)
    if not shift:
        return jsonify({'error': 'Not Found'}), 404
    
    user = User.query.get(request.user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if user.balance < shift.price:
        return jsonify({
            'error': 'Insufficient Balance',
            'message': f"Saldo tidak cukup. Butuh {shift.price}, saldo {user.balance}"
        }), 402
    
    user.balance -= shift.price
    
    trx = Transaction(
        user_id=user.id,
        shift_id=shift.id,
        amount=shift.price,
        status='SUCCESS'
    )
    db.session.add(trx)
    db.session.commit()
    
    return jsonify({
        'status': 'ok',
        'message': 'Shift berhasil dibeli',
        'shift_id': shift.id,
        'transaction_id': f"TRX-{trx.id}",
        'balance_after': f"Rp {user.balance:,}".replace(',', '.')
    }), 200

@shifts_bp.route('/api/v1/shift/<int:sid>/activate', methods=['POST'])
@require_auth
def activate_shift(sid):
    shift = Shift.query.get(sid)
    if not shift:
        return jsonify({'error': 'Not Found'}), 404
    
    user = User.query.get(request.user_id)
    trx = Transaction.query.filter_by(
        user_id=user.id, shift_id=sid, status='SUCCESS'
    ).first()
    
    if not trx:
        return jsonify({'error': 'Belum dibeli'}), 403
    
    trx.status = 'ACTIVATED'
    db.session.commit()
    
    return jsonify({
        'status': 'ok',
        'message': f'Shift {sid} diaktifkan',
        'shift': shift.to_dict()
    }), 200
