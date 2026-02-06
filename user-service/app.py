# uniCollab - User Service - file: app.py
from flask import Flask
from routes.auth import auth_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(auth_bp)

@app.route("/")
def home():
    return {"message": "User Service Running"}

@app.route("/health")
def health():
    return {"status": "user-service up"}

if __name__ == "__main__":
    app.run(port=5001, debug=True)
