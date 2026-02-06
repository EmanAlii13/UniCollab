# uniCollab - User Service - routes - file: auth.py
from flask import Blueprint, request, jsonify
import bcrypt
import jwt
import datetime
from models.user import User
from config import JWT_SECRET

auth_bp = Blueprint("auth_bp", __name__)

# ------------------ LOGIN ------------------
@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"message": "Email and password required"}), 400

    user_data = User.find_by_email(data["email"])
    if not user_data:
        return jsonify({"message": "Invalid credentials"}), 401

    if not bcrypt.checkpw(data["password"].encode(), user_data["password"].encode()):
        return jsonify({"message": "Invalid credentials"}), 401

    token_payload = {
        "user_id": str(user_data["_id"]),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(token_payload, JWT_SECRET, algorithm="HS256")

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": {
            "id": str(user_data["_id"]),
            "username": user_data["username"],
            "email": user_data["email"],
            "role": user_data.get("role"),
            "project_id": user_data.get("project_id"),
            "last_message": user_data.get("last_message"),
            "join_requests": user_data.get("join_requests", [])
        }
    }), 200

# ------------------ STATUS ------------------
@auth_bp.route("/user/status", methods=["GET"])
def user_status():
    return jsonify({"status": "User service endpoint working"}), 200

# ------------------ CREATE PROJECT ------------------
@auth_bp.route("/user/create-project", methods=["POST"])
def create_project():
    data = request.get_json()
    if not data or "user_id" not in data or "project_id" not in data:
        return jsonify({"message": "user_id and project_id required"}), 400

    user = User.find_by_id(data["user_id"])
    if not user:
        return jsonify({"message": "User not found"}), 404

    User.create_project(data["user_id"], data["project_id"])
    return jsonify({"message": "Project created successfully. User is now the owner"}), 200

# ------------------ JOIN PROJECT ------------------
@auth_bp.route("/user/join-project", methods=["POST"])
def join_project():
    data = request.get_json()
    if not data or "user_id" not in data or "owner_id" not in data or "project_id" not in data:
        return jsonify({"message": "user_id, owner_id and project_id required"}), 400

    user = User.find_by_id(data["user_id"])
    owner = User.find_by_id(data["owner_id"])
    if not user or not owner:
        return jsonify({"message": "User or Owner not found"}), 404

    User.send_join_request(data["user_id"], data["owner_id"])
    return jsonify({"message": "Join request sent to the project owner"}), 200

# ------------------ ACCEPT JOIN REQUEST ------------------
@auth_bp.route("/user/accept-request", methods=["POST"])
def accept_request():
    data = request.get_json()
    if not data or "owner_id" not in data or "user_id" not in data or "project_id" not in data:
        return jsonify({"message": "owner_id, user_id and project_id required"}), 400

    User.accept_join_request(data["owner_id"], data["user_id"], data["project_id"])
    return jsonify({"message": "User request accepted"}), 200

# ------------------ REJECT JOIN REQUEST ------------------
@auth_bp.route("/user/reject-request", methods=["POST"])
def reject_request():
    data = request.get_json()
    if not data or "owner_id" not in data or "user_id" not in data or "project_id" not in data:
        return jsonify({"message": "owner_id, user_id and project_id required"}), 400

    User.reject_join_request(data["owner_id"], data["user_id"], data["project_id"])
    return jsonify({"message": "User request rejected"}), 200

# ------------------ LEAVE PROJECT ------------------
@auth_bp.route("/user/leave-project", methods=["POST"])
def leave_project():
    data = request.get_json()
    if not data or "user_id" not in data:
        return jsonify({"message": "user_id required"}), 400

    user = User.find_by_id(data["user_id"])
    if not user:
        return jsonify({"message": "User not found"}), 404

    User.leave_project(data["user_id"])
    return jsonify({"message": "User left the project successfully"}), 200

# ------------------ UPDATE LAST MESSAGE ------------------
@auth_bp.route("/user/update-last-message", methods=["POST"])
def update_last_message():
    data = request.get_json()
    if not data or "user_id" not in data or "message" not in data:
        return jsonify({"message": "user_id and message required"}), 400

    user = User.find_by_id(data["user_id"])
    if not user:
        return jsonify({"message": "User not found"}), 404

    User.update_last_message(data["user_id"], data["message"])
    return jsonify({"message": "Last message updated successfully"}), 200
