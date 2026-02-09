# user-service/services/user_service.py

from passlib.context import CryptContext
from database import users_collection

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# =========================
# Password utilities
# =========================

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

# =========================
# User retrieval
# =========================

# ❗️الدالة الأصلية (نتركها كما هي بدون حذف)
def get_user_by_username(email: str):
    return users_collection.find_one({"email": email})

# ✅ دالة أوضح اسمًا (تحسين فقط)
def get_user_by_email(email: str):
    return users_collection.find_one({"email": email})

# =========================
# User rules (Microservice-safe)
# =========================

def can_join_project(email: str) -> bool:
    """
    يتحقق إذا كان المستخدم غير مرتبط بأي مشروع
    """
    user = get_user_by_email(email)
    if not user:
        return False
    return user.get("project_id") is None

def assign_project_to_user(email: str, project_id: str, role: str):
    """
    ربط المستخدم بمشروع (بدون معرفة تفاصيل المشروع)
    """
    users_collection.update_one(
        {"email": email},
        {
            "$set": {
                "project_id": project_id,
                "role": role
            }
        }
    )

def remove_project_from_user(email: str):
    """
    إزالة ربط المستخدم بالمشروع
    """
    users_collection.update_one(
        {"email": email},
        {
            "$set": {
                "project_id": None,
                "role": None
            }
        }
    )

# =========================
# Existing functionality (بدون تعديل)
# =========================

def update_user_project_id(email: str, project_id: str):
    """تحديث project_id للطالب"""
    users_collection.update_one(
        {"email": email},
        {"$set": {"project_id": project_id}}
    )
