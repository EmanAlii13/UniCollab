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
