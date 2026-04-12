import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
from jose import jwt

from app.config import settings

ACCESS = "access"
REFRESH = "refresh"


def hash_password(password: str) -> str:
    # bcrypt limit: 72 bytes
    pw = password.encode("utf-8")[:72]
    return bcrypt.hashpw(pw, bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    pw = plain.encode("utf-8")[:72]
    try:
        return bcrypt.checkpw(pw, hashed.encode("utf-8"))
    except ValueError:
        return False


def _make_token(subject: str, token_type: str, expires: timedelta) -> tuple[str, str]:
    jti = str(uuid.uuid4())
    expire = datetime.now(timezone.utc) + expires
    payload: dict[str, Any] = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "jti": jti,
        "type": token_type,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token, jti


def create_access_token(subject: str | uuid.UUID) -> tuple[str, str]:
    return _make_token(
        str(subject), ACCESS, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )


def create_refresh_token(subject: str | uuid.UUID) -> tuple[str, str]:
    return _make_token(
        str(subject), REFRESH, timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
