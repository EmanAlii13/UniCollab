# user-service/services/user_service.py
from passlib.context import CryptContext
from database import users_collection
from typing import Optional, Literal
import logging

# =========================
# Logging Configuration
# =========================

logger = logging.getLogger(__name__)

# =========================
# Password utilities
# =========================

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

# =========================
# User retrieval
# =========================

def get_user_by_email(email: str) -> Optional[dict]:
    return users_collection.find_one({"email": email})

def get_user_by_username(email: str) -> Optional[dict]:
    logger.warning("get_user_by_username is deprecated. Use get_user_by_email instead.")
    return get_user_by_email(email)

# =========================
# User rules (Microservice-safe)
# =========================

def can_join_project(email: str) -> bool:
    user = get_user_by_email(email)
    if not user:
        logger.warning(f"can_join_project called for non-existing user: {email}")
        return False
    return user.get("project_id") is None

def assign_project_to_user(email: str, project_id: str, role: Literal["leader", "member"]) -> None:
    users_collection.update_one(
        {"email": email},
        {"$set": {"project_id": project_id, "role": role}}
    )
    logger.info(f"Assigned project {project_id} to user {email} with role {role}")

def remove_project_from_user(email: str) -> None:
    users_collection.update_one(
        {"email": email},
        {"$set": {"project_id": None, "role": None}}
    )
    logger.info(f"Removed project from user {email}")

# =========================
# Existing functionality (بدون حذف)
# =========================

def update_user_project_id(email: str, project_id: str) -> None:
    users_collection.update_one(
        {"email": email},
        {"$set": {"project_id": project_id}}
    )
    logger.info(f"Updated project_id for user {email} to {project_id}")
