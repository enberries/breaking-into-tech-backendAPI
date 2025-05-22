from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from models import User, Profile  # Import Profile model
import jwt
import datetime
import os  # Add this import to access environment variables

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
    auth_header = request.headers.get('Authorization')
    
    print(auth_header)

    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Bearer token is missing or invalid"}), 401

    token = auth_header.split(' ')[1]  # Extract the token part

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

@routes.route('/profile', methods=['PUT'])
def update_profile():
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Bearer token is missing or invalid"}), 401

    token = auth_header.split(' ')[1]  # Extract the token part

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

        # Get the updated data from the request
        data = request.get_json()

        # Update profile fields
        profile.firstname = data.get('firstname', profile.firstname)
        profile.lastname = data.get('lastname', profile.lastname)
        profile.bio = data.get('bio', profile.bio)
        profile.profile_picture = data.get('profile_picture', profile.profile_picture)

        # Commit changes to the database
        db.session.commit()

        return jsonify({"message": "Profile updated successfully"})

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

@routes.route('/change-password', methods=['PUT'])
def change_password():
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Bearer token is missing or invalid"}), 401

    token = auth_header.split(' ')[1]  # Extract the token part

    try:
        # Decode the JWT token
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token['user_id']

        # Fetch user from the database
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Get the updated password data from the request
        data = request.get_json()
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if not old_password or not new_password or not confirm_password:
            return jsonify({"error": "old_password, new_password, and confirm_password are required"}), 400

        if not check_password_hash(user.password_hash, old_password):
            return jsonify({"error": "Old password is incorrect"}), 400

        if new_password != confirm_password:
            return jsonify({"error": "Passwords do not match"}), 400

        # Update the user's password
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()

        return jsonify({"message": "Password changed successfully"})

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

@routes.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"error": "Email is required"}), 400

    # Check if user exists
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User with this email does not exist"}), 404

    # Generate a reset token
    reset_token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=int(os.getenv('RESET_TOKEN_EXPIRATION_MINUTES', 5)))  # Default to 5 minutes if not set
    }, SECRET_KEY, algorithm='HS256')

    # Store the token in the database for one-time use
    user.reset_token = reset_token
    db.session.commit()

    return jsonify({
        "message": "Password token generated successfully",
        "token": reset_token
    })

@routes.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')

    if not token or not new_password or not confirm_password:
        return jsonify({"error": "Token, new_password, and confirm_password are required"}), 400

    if new_password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    try:
        # Decode the reset token
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token['user_id']

        # Fetch user from the database
        user = User.query.get(user_id)
        if not user or user.reset_token != token:
            return jsonify({"error": "Invalid or already used token"}), 401

        # Update the user's password
        user.password_hash = generate_password_hash(new_password)
        user.reset_token = None  # Invalidate the token after use
        db.session.commit()

        return jsonify({"message": "Password reset successfully"})

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
