# user-service/routes/auth.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal
import logging

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
# Logging
# =========================

logger = logging.getLogger(__name__)

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
    role: Literal["leader", "member"]

# =========================
# Helper
# =========================

def serialize_user(user: dict) -> dict:
    if "_id" in user:
        user["_id"] = str(user["_id"])
    return user

# =========================
# Endpoints
# =========================

@router.post("/login")
def login(data: LoginRequest):
    user = get_user_by_email(data.email)
    if not user:
        logger.warning(f"Login attempt failed - user not found: {data.email}")
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(data.password, user["password"]):
        logger.warning(f"Login failed - wrong password for: {data.email}")
        raise HTTPException(status_code=401, detail="Wrong password")

    message = user.get("last_message")
    if message:
        users_collection.update_one({"email": data.email}, {"$set": {"last_message": None}})
        logger.info(f"Cleared last_message for user {data.email}")

    logger.info(f"User logged in successfully: {data.email}")
    return serialize_user({
        "username": user["username"],
        "role": user.get("role"),
        "project_id": user.get("project_id"),
        "last_message": message
    })


@router.post("/logout")
def logout(data: LogoutRequest):
    user = get_user_by_email(data.email)
    if not user:
        logger.warning(f"Logout failed - user not found: {data.email}")
        raise HTTPException(status_code=404, detail="User not found")

    logger.info(f"User logged out: {data.email}")
    return {"message": f"User {user['username']} logged out successfully."}


@router.get("/me")
def get_user(email: str):
    user = get_user_by_email(email)
    if not user:
        logger.warning(f"/me request - user not found: {email}")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"/me accessed for user: {email}")
    return serialize_user(user)


@router.get("/users/{email}/status")
def user_status(email: str):
    user = get_user_by_email(email)
    if not user:
        logger.warning(f"Status check failed - user not found: {email}")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Status checked for user: {email}")
    return serialize_user({
        "email": user["email"],
        "project_id": user.get("project_id"),
        "role": user.get("role"),
        "can_join_project": user.get("project_id") is None
    })


@router.post("/users/{email}/assign-project")
def assign_project(email: str, data: AssignProjectRequest):
    user = get_user_by_email(email)
    if not user:
        logger.warning(f"Assign project failed - user not found: {email}")
        raise HTTPException(status_code=404, detail="User not found")
    if not can_join_project(email):
        logger.warning(f"Assign project blocked - user already assigned: {email}")
        raise HTTPException(status_code=400, detail="User already assigned to a project")

    assign_project_to_user(email, data.project_id, data.role)
    logger.info(f"Project {data.project_id} assigned to user {email} as {data.role}")
    return {"message": "Project assigned to user successfully"}


@router.post("/users/{email}/remove-project")
def remove_project(email: str):
    user = get_user_by_email(email)
    if not user:
        logger.warning(f"Remove project failed - user not found: {email}")
        raise HTTPException(status_code=404, detail="User not found")

    remove_project_from_user(email)
    logger.info(f"Project removed from user {email}")
    return {"message": "User removed from project successfully"}
