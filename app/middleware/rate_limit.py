from functools import wraps
from flask import request, jsonify
from datetime import datetime

REQUESTS = {}
MAX_PER_MINUTE = 5

def rate_limit(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        uid = request.headers.get('X-User-Id', 'anonymous')
        now = datetime.now().timestamp()
        
        if uid not in REQUESTS:
            REQUESTS[uid] = []
        
        REQUESTS[uid] = [t for t in REQUESTS[uid] if now - t < 60]
        
        if len(REQUESTS[uid]) >= MAX_PER_MINUTE:
            return jsonify({
                'error': 'Too Many Requests',
                'message': f'Maks {MAX_PER_MINUTE} request/menit'
            }), 429
        
        REQUESTS[uid].append(now)
        return f(*args, **kwargs)
    return decorated
