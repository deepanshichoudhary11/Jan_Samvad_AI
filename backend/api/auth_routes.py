from flask import Blueprint, request, jsonify
import json
import os

auth_bp = Blueprint('auth', __name__)

def load_users():
    with open('data/users.json', 'r') as f:
        return json.load(f)

def save_users(users):
    with open('data/users.json', 'w') as f:
        json.dump(users, f, indent=2)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validation
    required_fields = ['fullName', 'mobile', 'email', 'password', 'confirmPassword']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    if data['password'] != data['confirmPassword']:
        return jsonify({'error': 'Passwords do not match'}), 400
    
    users = load_users()
    
    # Check if user already exists
    for user in users:
        if user['email'] == data['email'] or user['mobile'] == data['mobile']:
            return jsonify({'error': 'User already exists'}), 400
    
    # Create new user
    new_user = {
        'id': str(len(users) + 1),
        'fullName': data['fullName'],
        'email': data['email'],
        'mobile': data['mobile'],
        'password': data['password']
    }
    
    users.append(new_user)
    save_users(users)
    
    return jsonify({
        'message': 'Registration successful',
        'user': {
            'id': new_user['id'],
            'fullName': new_user['fullName'],
            'email': new_user['email'],
            'mobile': new_user['mobile']
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    users = load_users()
    
    # Find user by email or mobile
    user = None
    for u in users:
        if u['email'] == data['email'] or u['mobile'] == data['email']:
            user = u
            break
    
    if not user or user['password'] != data['password']:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    return jsonify({
        'message': 'Login successful',
        'user': {
            'id': user['id'],
            'fullName': user['fullName'],
            'email': user['email'],
            'mobile': user['mobile']
        }
    }), 200 