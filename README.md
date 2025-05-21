# Breaking Into Tech Backend API

A simple Flask-based API for the Breaking Into Tech platform.

## Features

- **Root Endpoint**: Returns a greeting message and current timestamp
- **Health Check**: Provides service status information

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
   python -m venv .venv
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

## Running the Application

Start the Flask development server:
```bash
python3 api.py
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

## Development

To extend this API, add new routes in the `api.py` file following the existing pattern.

## License

[Your License Information]