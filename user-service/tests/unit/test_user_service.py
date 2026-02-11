# user-service/tests/unit/test_user_service.py

import pytest
from services import user_service

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
# Fixtures
# =========================

@pytest.fixture
def mock_collection(monkeypatch):
    mock_db = MockUsersCollection()

    # مستخدم بدون مشروع
    mock_db.insert_one({
        "email": "test@uni.edu",
        "project_id": None,
        "role": None
    })

    # مستخدم مرتبط بمشروع
    mock_db.insert_one({
        "email": "assigned@uni.edu",
        "project_id": "project123",
        "role": "member"
    })

    # Replace real collection with mock
    monkeypatch.setattr(user_service, "users_collection", mock_db)

    return mock_db


# =========================
# Tests
# =========================

def test_can_join_project_true(mock_collection):
    assert user_service.can_join_project("test@uni.edu") is True


def test_can_join_project_false(mock_collection):
    assert user_service.can_join_project("assigned@uni.edu") is False


def test_assign_project_to_user(mock_collection):
    user_service.assign_project_to_user(
        email="test@uni.edu",
        project_id="project999",
        role="leader"
    )

    user = mock_collection.find_one({"email": "test@uni.edu"})
    assert user["project_id"] == "project999"
    assert user["role"] == "leader"


def test_remove_project_from_user(mock_collection):
    user_service.remove_project_from_user("assigned@uni.edu")

    user = mock_collection.find_one({"email": "assigned@uni.edu"})
    assert user["project_id"] is None
    assert user["role"] is None
