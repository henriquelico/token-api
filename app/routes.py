from flask import request, jsonify
from app import app, db
from app.jwt_utils import generate_token, token_required

@app.route('/generate_token', methods=['POST'])
def generate_token_route():
    data = request.get_json()
    client_id = data.get('client_id')
    client_secret = data.get('client_secret')
    
    if not client_id or not client_secret:
        return jsonify({'message': 'Client ID and client secret are required!'}), 400

    token = generate_token(client_id, client_secret)
    return jsonify({'access_token': token.decode('utf-8')})

@app.route('/protected', methods=['GET'])
@token_required
def protected_route(current_user):
    return jsonify({'message': f'Hello, {current_user["sub"]}! This is a protected route.'})
