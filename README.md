# Breaking Into Tech Backend API

A simple Flask-based API for the Breaking Into Tech platform.

## Features

- **Root Endpoint**: Returns a greeting message and current timestamp
- **Health Check**: Provides service status information
- **Signup**: Register a new user

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- PostgreSQL database

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd breaking-into-tech-backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python3 -m venv .venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     /venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Configure your database by creating a `.env` file in the project root:
   ```bash
   DB_USER=your_postgres_username
   DB_PASSWORD=your_postgres_password
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=breaking_into_tech
   ```

6. Create the PostgreSQL database:
   ```bash
   createdb breaking_into_tech
   ```
   If you don't have permissions, use:
   ```bash
   sudo -u postgres createdb breaking_into_tech
   ```

## Database Migration

To run database migrations (create/update tables):

```bash
chmod +x migrate.sh
./migrate.sh
```

## Running the Application

To start the Flask application as a background service:

```bash
chmod +x flask_service.sh
./flask_service.sh start
```

To stop the service:

```bash
./flask_service.sh stop
```

To check the status:

```bash
./flask_service.sh status
```

### Managing Logs

The Flask service writes logs to `/tmp/flask_app.log` (or similar, see `flask_service.sh`).
To view the logs in real time:

```bash
tail -f /tmp/flask_app.log
```

The server will run on `http://127.0.0.1:5000/` (localhost) by default with debug mode enabled.

## API Endpoints

### 1. Root Endpoint

- **URL**: `/`
- **Method**: GET
- **Response Example**:
  ```json
  {
    "message": "Hello, Flask!",
    "timestamp": "2025-05-15 14:30:45"
  }
  ```

### 2. Health Check

- **URL**: `/health`
- **Method**: GET
- **Response Example**:
  ```json
  {
    "status": "healthy",
    "service": "breaking-into-tech-backend",
    "database": {
      "status": "healthy",
      "error": null
    },
    "timestamp": "2025-05-15 14:30:45"
  }
  ```

### 3. Signup

- **URL**: `/signup`
- **Method**: POST
- **Request Body Example**:
  ```json
  {
    "firstname": "John",
    "lastname": "Doe",
    "email": "john@example.com",
    "password": "yourpassword",
    "bio": "Optional bio",
    "profile_picture": "Optional URL"
  }
  ```
- **Success Response Example**:
  ```json
  {
    "message": "User registered successfully",
    "user_id": 1
  }
  ```
- **Error Response Example** (missing field):
  ```json
  {
    "error": "Missing required field: firstname"
  }
  ```
- **Error Response Example** (duplicate email):
  ```json
  {
    "error": "Email already registered"
  }
  ```

## Development

To extend this API, add new routes in the `api.py` file following the existing pattern.

## License

[Your License Information]