import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.user import Role


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: Role = Role.PAGE_EDITOR
    is_active: bool = True
    avatar_url: str | None = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: str | None = None
    avatar_url: str | None = None
    role: Role | None = None
    is_active: bool | None = None
    password: str | None = None


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    is_verified: bool
    last_login: datetime | None
    created_at: datetime
    updated_at: datetime


class ProfileUpdate(BaseModel):
    """User self-update — only name and avatar."""
    full_name: str | None = None
    avatar_url: str | None = None


class PasswordChange(BaseModel):
    current_password: str
    new_password: str
