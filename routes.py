from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from database import db
from models import User

routes = Blueprint('routes', __name__)

@routes.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    required_fields = ['firstname', 'lastname', 'email', 'password']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409

    hashed_password = generate_password_hash(data['password'])
    user = User(
        firstname=data['firstname'],
        lastname=data['lastname'],
        email=data['email'],
        password_hash=hashed_password,
        bio=data.get('bio'),
        profile_picture=data.get('profile_picture')
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully', 'user_id': user.id}), 201
