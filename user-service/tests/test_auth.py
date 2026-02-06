# uniCollab - User Service - tests - file: test_auth.py
import unittest
import json
from app import app
from models.user import User
from bson.objectid import ObjectId
from database import client  # لإغلاق الاتصال بعد الاختبارات

class TestAuthRoutes(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        client.close()  # يغلق اتصال MongoDB بعد كل الاختبارات

    def setUp(self):
        self.client = app.test_client()
        self.test_user_id = None
        self.owner_id = None
        self.project_id = "proj_test"

        # اختيار مستخدمين موجودين مسبقًا في قاعدة البيانات
        test_user = User.find_by_email("s1@uni.edu")
        self.test_user_id = str(test_user["_id"])

        owner_user = User.find_by_email("s2@uni.edu")
        self.owner_id = str(owner_user["_id"])

    # ------------------ LOGIN ------------------
    def test_login_success(self):
        response = self.client.post(
            "/auth/login",
            data=json.dumps({"email": "s1@uni.edu", "password": "pass1"}),  # كلمة المرور الصحيحة
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("token", data)
        self.assertEqual(data["user"]["email"], "s1@uni.edu")

    def test_login_fail_wrong_password(self):
        response = self.client.post(
            "/auth/login",
            data=json.dumps({"email": "s1@uni.edu", "password": "wrongpass"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 401)

    # ------------------ CREATE PROJECT ------------------
    def test_create_project(self):
        response = self.client.post(
            "/user/create-project",
            data=json.dumps({"user_id": self.owner_id, "project_id": self.project_id}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        owner_data = User.find_by_id(self.owner_id)
        self.assertEqual(owner_data["project_id"], self.project_id)
        self.assertEqual(owner_data["role"], "owner")

    # ------------------ JOIN / ACCEPT / REJECT ------------------
    def test_join_project_request(self):
        response = self.client.post(
            "/user/join-project",
            data=json.dumps({"user_id": self.test_user_id, "owner_id": self.owner_id, "project_id": self.project_id}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        owner_data = User.find_by_id(self.owner_id)
        self.assertIn(self.test_user_id, owner_data.get("join_requests", []))

    def test_accept_request(self):
        response = self.client.post(
            "/user/accept-request",
            data=json.dumps({"owner_id": self.owner_id, "user_id": self.test_user_id, "project_id": self.project_id}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        user_data = User.find_by_id(self.test_user_id)
        self.assertEqual(user_data["project_id"], self.project_id)
        self.assertEqual(user_data["role"], "member")
        self.assertIsNotNone(user_data["last_message"])
        owner_data = User.find_by_id(self.owner_id)
        self.assertNotIn(self.test_user_id, owner_data.get("join_requests", []))

    def test_reject_request(self):
        fake_user_id = str(ObjectId())
        User.send_join_request(fake_user_id, self.owner_id)

        response = self.client.post(
            "/user/reject-request",
            data=json.dumps({"owner_id": self.owner_id, "user_id": fake_user_id, "project_id": self.project_id}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        owner_data = User.find_by_id(self.owner_id)
        self.assertNotIn(fake_user_id, owner_data.get("join_requests", []))

    # ------------------ LEAVE PROJECT ------------------
    def test_leave_project(self):
        response = self.client.post(
            "/user/leave-project",
            data=json.dumps({"user_id": self.test_user_id}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        user_data = User.find_by_id(self.test_user_id)
        self.assertIsNone(user_data["project_id"])
        self.assertIsNone(user_data["role"])
        self.assertIsNone(user_data["last_message"])

    # ------------------ UPDATE LAST MESSAGE ------------------
    def test_update_last_message(self):
        message = "Hello from unit test"
        response = self.client.post(
            "/user/update-last-message",
            data=json.dumps({"user_id": self.test_user_id, "message": message}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        user_data = User.find_by_id(self.test_user_id)
        self.assertEqual(user_data["last_message"], message)

if __name__ == "__main__":
    unittest.main()
