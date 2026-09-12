from flask import Blueprint, jsonify, request
from app.models import db
from app.models.user import User
import hmac, hashlib, base64, json, time, os

auth_bp = Blueprint('auth', __name__)
SECRET = os.environ.get('SECRET_KEY', 'rahasia_super_kuat_123').encode()

def sign_token(payload):
    data = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    sig = hmac.new(SECRET, data.encode(), hashlib.sha256).hexdigest()
    return f"{data}.{sig}"

def verify_token(token):
    try:
        data, sig = token.rsplit(".", 1)
        expected = hmac.new(SECRET, data.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected):
            return None
        payload = json.loads(base64.urlsafe_b64decode(data))
        if payload.get("exp", 0) < time.time():
            return None
        return payload
    except:
        return None

@auth_bp.route('/api/v1/login', methods=['POST'])
def login():
    body = request.get_json() or {}
    user_id = body.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'user_id required'}), 400
    
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify({'error': 'user not found'}), 404
    
    token = sign_token({
        'user_id': user.id,
        'exp': time.time() + 3600
    })
    
    return jsonify({'token': token, 'user': user.to_dict()})

