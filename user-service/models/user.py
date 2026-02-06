# uniCollab - User Service - models - file: user.py
from database import users_collection
from bson.objectid import ObjectId

class User:
    def __init__(self, data):
        self.id = str(data.get("_id"))
        self.username = data.get("username")
        self.email = data.get("email")
        self.password = data.get("password")
        self.role = data.get("role")
        self.project_id = data.get("project_id")
        self.last_message = data.get("last_message")
        self.join_requests = data.get("join_requests", [])  # طلبات الانضمام

    @staticmethod
    def find_by_email(email):
        return users_collection.find_one({"email": email})

    @staticmethod
    def find_by_id(user_id):
        return users_collection.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def join_project(user_id, project_id, role="member"):
        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"project_id": project_id, "role": role}}
        )

    @staticmethod
    def leave_project(user_id):
        user_data = User.find_by_id(user_id)
        if user_data and user_data.get("project_id"):
            project_id = user_data.get("project_id")
            # إزالة أي رسائل قديمة مرتبطة بالمشروع
            users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"project_id": None, "role": None, "last_message": None}}
            )

    @staticmethod
    def create_project(user_id, project_id):
        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"project_id": project_id, "role": "owner"}}
        )

    @staticmethod
    def update_last_message(user_id, message):
        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"last_message": message}}
        )

    # ------------------ Requests Handling ------------------
    @staticmethod
    def send_join_request(user_id, owner_id):
        users_collection.update_one(
            {"_id": ObjectId(owner_id)},
            {"$push": {"join_requests": user_id}}
        )

    @staticmethod
    def accept_join_request(owner_id, user_id, project_id):
        # إزالة من join_requests عند الـ Owner
        users_collection.update_one(
            {"_id": ObjectId(owner_id)},
            {"$pull": {"join_requests": user_id}}
        )
        # انضمام المستخدم للمشروع
        User.join_project(user_id, project_id)
        # وضع الرسالة مباشرة في last_message
        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"last_message": f"Your request to join project {project_id} was accepted"}}
        )

    @staticmethod
    def reject_join_request(owner_id, user_id, project_id):
        # إزالة من join_requests عند الـ Owner
        users_collection.update_one(
            {"_id": ObjectId(owner_id)},
            {"$pull": {"join_requests": user_id}}
        )
        # وضع الرسالة مباشرة في last_message
        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"last_message": f"Your request to join project {project_id} was rejected"}}
        )

    @staticmethod
    def get_status(user_id):
        user_data = User.find_by_id(user_id)
        if not user_data:
            return None
        return {
            "username": user_data.get("username"),
            "role": user_data.get("role"),
            "project_id": user_data.get("project_id"),
            "last_message": user_data.get("last_message"),
            "join_requests": user_data.get("join_requests", [])
        }
