# user-service/tests/integration/test_auth_routes.py

from fastapi.testclient import TestClient
from app import app
from services import user_service
from routes import auth

# =========================
# Mock Users Collection
# =========================

class MockUsersCollection:
    def __init__(self):
        self.users = {}

    def find_one(self, query):
        return self.users.get(query.get("email"))

    def update_one(self, query, update):
        email = query.get("email")
        if email in self.users:
            for key, value in update["$set"].items():
                self.users[email][key] = value

    def insert_one(self, user):
        self.users[user["email"]] = user


# =========================
# Test Setup
# =========================

client = TestClient(app)


def setup_module():
    """
    تجهيز Mock DB قبل تشغيل الاختبارات
    """
    mock_db = MockUsersCollection()

    # مستخدم صالح
    mock_db.insert_one({
        "username": "testuser",
        "email": "test@uni.edu",
        "password": user_service.hash_password("correctpass"),
        "project_id": None,
        "role": None,
        "last_message": "Welcome!"
    })

    # استبدال collection الحقيقي
    user_service.users_collection = mock_db
    auth.users_collection = mock_db


# =========================
# Tests
# =========================

def test_login_success():
    response = client.post(
        "/login",
        json={
            "email": "test@uni.edu",
            "password": "correctpass"
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert data["username"] == "testuser"
    assert data["project_id"] is None
    assert data["last_message"] == "Welcome!"


def test_login_wrong_password():
    response = client.post(
        "/login",
        json={
            "email": "test@uni.edu",
            "password": "wrongpass"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Wrong password"


def test_login_user_not_found():
    response = client.post(
        "/login",
        json={
            "email": "missing@uni.edu",
            "password": "pass"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
