#user-service/routes/auth.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.user_service import (
    get_user_by_username,
    get_user_by_email,
    verify_password,
    can_join_project,
    assign_project_to_user,
    remove_project_from_user
)
from database import users_collection

router = APIRouter()

# =========================
# Models
# =========================

class LoginRequest(BaseModel):
    email: str
    password: str

class LogoutRequest(BaseModel):
    email: str

class AssignProjectRequest(BaseModel):
    project_id: str
    role: str  # leader / member

# =========================
# Helper
# =========================

def serialize_user(user: dict) -> dict:
    """
    تحويل أي ObjectId في user إلى string قبل الإرجاع
    """
    if "_id" in user:
        user["_id"] = str(user["_id"])
    return user

# =========================
# Existing Endpoints
# =========================

@router.post("/login")
def login(data: LoginRequest):
    user = get_user_by_username(data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Wrong password")

    message = user.get("last_message")
    if message:
        users_collection.update_one(
            {"email": data.email},
            {"$set": {"last_message": None}}
        )

    return serialize_user({
        "username": user["username"],
        "role": user.get("role"),
        "project_id": user.get("project_id"),
        "last_message": message
    })

@router.post("/logout")
def logout(data: LogoutRequest):
    user = get_user_by_username(data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": f"User {user['username']} logged out successfully."}

@router.get("/me")
def get_user(email: str):
    user = get_user_by_username(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return serialize_user(user)

# =========================
# Internal Service-to-Service Endpoints
# =========================

@router.get("/users/{email}/status")
def user_status(email: str):
    """
    يستخدمه Project Service للتحقق من حالة المستخدم
    """
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return serialize_user({
        "email": user["email"],
        "project_id": user.get("project_id"),
        "role": user.get("role"),
        "can_join_project": user.get("project_id") is None
    })

@router.post("/users/{email}/assign-project")
def assign_project(email: str, data: AssignProjectRequest):
    """
    ربط المستخدم بمشروع (يستدعى من Project Service)
    """
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not can_join_project(email):
        raise HTTPException(
            status_code=400,
            detail="User already assigned to a project"
        )

    assign_project_to_user(email, data.project_id, data.role)

    return {"message": "Project assigned to user successfully"}

@router.post("/users/{email}/remove-project")
def remove_project(email: str):
    """
    فك ربط المستخدم من المشروع (انسحاب / حذف مشروع)
    """
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    remove_project_from_user(email)

    return {"message": "User removed from project successfully"}
