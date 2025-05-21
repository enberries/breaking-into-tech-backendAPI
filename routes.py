from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from models import User, Profile  # Import Profile model
import jwt
import datetime

# Secret key for JWT encoding/decoding
SECRET_KEY = "your_secret_key"

routes = Blueprint('routes', __name__)

@routes.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    required_fields = ['firstname', 'lastname', 'email', 'password', 'entity']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409

    hashed_password = generate_password_hash(data['password'])

    # Create User and Profile entries
    user = User(
        email=data['email'],
        password_hash=hashed_password,
        entity=data['entity']
    )
    print(user)
    db.session.add(user)
    db.session.flush()  # Flush to get the user ID for the profile

    profile = Profile(
        user_id=user.id,
        firstname=data['firstname'],
        lastname=data['lastname'],
        bio=data.get('bio'),
        profile_picture=data.get('profile_picture')
    )
    db.session.add(profile)
    db.session.commit()

    return jsonify({'message': 'User registered successfully', 'user_id': user.id}), 201

@routes.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()

    # Validate input
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400

    # Fetch user from the database
    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({"error": "Invalid email or password"}), 401

    # Generate JWT token
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, SECRET_KEY, algorithm='HS256')

    return jsonify({"message": "Login successful", "token": token})

@routes.route('/profile', methods=['GET'])
def get_profile():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({"error": "Token is missing"}), 401

    try:
        # Decode the JWT token
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token['user_id']

        # Fetch user and profile details from the database
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        profile = Profile.query.filter_by(user_id=user_id).first()
        if not profile:
            return jsonify({"error": "Profile not found"}), 404

        # Return user profile details
        return jsonify({
            "email": user.email,
            "firstname": profile.firstname,
            "lastname": profile.lastname,
            "bio": profile.bio,
            "profile_picture": profile.profile_picture,
            "entity": user.entity
        })

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
