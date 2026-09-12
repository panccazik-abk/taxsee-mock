from flask import Blueprint, jsonify, request
from app.models import db
from app.models.user import User
from app.models.transaction import Transaction
from app.middleware.auth import require_auth

balance_bp = Blueprint('balance', __name__)

@balance_bp.route('/api/v1/balance', methods=['GET'])
@require_auth
def get_balance():
    user = User.query.get(request.user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200

@balance_bp.route('/api/v1/topup', methods=['POST'])
@require_auth
def topup():
    body = request.get_json() or {}
    amount = int(body.get('amount', 0))
    
    if amount <= 0:
        return jsonify({'error': 'Amount harus > 0'}), 400
    
    user = User.query.get(request.user_id)
    user.balance += amount
    
    trx = Transaction(
        user_id=user.id,
        amount=amount,
        status='TOPUP'
    )
    db.session.add(trx)
    db.session.commit()
    
    return jsonify({
        'status': 'ok',
        'message': 'Topup berhasil',
        'amount': f"Rp {amount:,}".replace(',', '.'),
        'balance_after': f"Rp {user.balance:,}".replace(',', '.')
    }), 200

@balance_bp.route('/api/v1/transactions', methods=['GET'])
@require_auth
def get_transactions():
    user = User.query.get(request.user_id)
    trxs = Transaction.query.filter_by(user_id=user.id).order_by(
        Transaction.created_at.desc()
    ).limit(50).all()
    return jsonify({'transactions': [t.to_dict() for t in trxs]}), 200
