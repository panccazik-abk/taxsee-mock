from functools import wraps
from flask import request, jsonify
from app.routes.auth import verify_token

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            return jsonify({'error': 'No token'}), 401
        token = auth.replace('Bearer ', '')
        payload = verify_token(token)
        if not payload:
            return jsonify({'error': 'Invalid token'}), 401
        request.user_id = payload.get('user_id')
        return f(*args, **kwargs)
    return decorated
