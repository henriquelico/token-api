import jwt
import datetime
from functools import wraps
from flask import jsonify, request

def generate_token(client_id, client_secret):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {
        'exp': expiration_time,
        'iat': datetime.datetime.utcnow(),
        'sub': client_id,
        'client_secret': client_secret
    }
    token = jwt.encode(payload, 'your_secret_key', algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(data, *args, **kwargs)

    return decorated
