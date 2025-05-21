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

### Updated Signup API

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
      "profile_picture": "Optional URL",
      "entity": "project_name_or_organization"
  }
  ```

- **Explanation**:
  - The `entity` field is used to associate the user with a specific project or organization, enabling multi-project support.
  - Authentication data (`email`, `password`) is stored in the `User` table.
  - Profile details (`firstname`, `lastname`, `bio`, `profile_picture`) are stored in the `Profile` table.

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

### 4. Signin

- **URL**: `/signin`
- **Method**: POST

- **Request Body Example**:

  ```json
  {
      "email": "john@example.com",
      "password": "yourpassword"
  }
  ```

- **Explanation**:
  - Authenticates the user by validating the email and password.
  - Returns a JWT token upon successful authentication.

- **Success Response Example**:

  ```json
  {
      "message": "Login successful",
      "token": "<jwt_token>"
  }
  ```

- **Error Response Example** (invalid credentials):

  ```json
  {
      "error": "Invalid email or password"
  }
  ```

- **Error Response Example** (missing fields):

  ```json
  {
      "error": "Email and password are required"
  }
  ```

### 5. Get Profile

- **URL**: `/profile`
- **Method**: GET

- **Headers**:
  - `Authorization`: Bearer `<your_jwt_token>`

- **Explanation**:
  - Retrieves the user's profile details using the JWT token provided in the `Authorization` header.
  - The token is decoded to fetch the user ID, and the corresponding user and profile details are retrieved from the database.

- **Success Response Example**:

  ```json
  {
      "email": "john@example.com",
      "firstname": "John",
      "lastname": "Doe",
      "bio": "Optional bio",
      "profile_picture": "Optional URL",
      "entity": "project_name_or_organization"
  }
  ```

- **Error Response Example** (missing token):

  ```json
  {
      "error": "Token is missing"
  }
  ```

- **Error Response Example** (invalid token):

  ```json
  {
      "error": "Invalid token"
  }
  ```

- **Error Response Example** (user not found):

  ```json
  {
      "error": "User not found"
  }
  ```

## Development

To extend this API, add new routes in the `api.py` file following the existing pattern.

## License

[Your License Information]