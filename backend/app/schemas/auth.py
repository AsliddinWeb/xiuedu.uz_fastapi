from pydantic import BaseModel, EmailStr

from app.schemas.user import UserOut


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserOut


class AccessToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
