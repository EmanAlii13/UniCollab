# user-service/models/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional, Literal

class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    project_id: Optional[str] = None
    role: Optional[Literal["leader", "member", None]] = None
    last_message: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "username": "student1",
                "email": "student1@uni.edu",
                "password": "hashed_password_here",
                "project_id": None,
                "role": None,
                "last_message": None
            }
        }
