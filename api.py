from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def hello():
    return jsonify({
        "message": "Hello, Flask!",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route("/health")
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "breaking-into-tech-backend",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
