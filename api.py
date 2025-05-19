from flask import Flask, jsonify, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from database import db

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Database configuration
# Get values from .env file
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# Configure SQLAlchemy
# URL encode the password to handle special characters
from urllib.parse import quote_plus
encoded_password = quote_plus(DB_PASSWORD)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db.init_app(app)
from models import User  # Import after db.init_app(app)

migrate = Migrate(app, db)

# Flag to track database availability
db_available = True

# For Flask 2.0+ we need to use app.before_request instead
# and run the check only once
_db_check_performed = False

@app.before_request
def check_db_connection():
    global db_available, _db_check_performed
    
    # Only run this check once
    if _db_check_performed:
        return None
    
    _db_check_performed = True
    try:
        from sqlalchemy import text
        # Try a simple database query
        db.session.execute(text("SELECT 1"))
        db_available = True
        print("Database connection successful")
    except Exception as e:
        db_available = False
        print(f"Database connection failed: {e}")
        print("Application will continue running with limited functionality")

@app.route("/")
def hello():
    return jsonify({
        "message": "Hello, Flask!",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route("/health")
def health_check():
    # Check database connection
    db_status = "healthy"
    db_error = None
    
    try:
        # Execute a simple query to check connection
        from sqlalchemy import text
        db.session.execute(text("SELECT 1"))
    except Exception as e:
        db_status = "unhealthy"
        db_error = str(e)
    
    return jsonify({
        "status": "healthy" if db_error is None else "unhealthy",
        "service": "breaking-into-tech-backend",
        "database": {
            "status": db_status,
            "error": db_error
        },
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
