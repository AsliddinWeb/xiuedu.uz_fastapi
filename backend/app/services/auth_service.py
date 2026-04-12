import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.user import User
from app.redis_client import redis_client
from app.schemas.auth import TokenPair
from app.utils.security import (
    ACCESS,
    REFRESH,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)

BLACKLIST_PREFIX = "auth:blacklist:"


# ---------- helpers ----------

async def _blacklist_jti(jti: str, exp_ts: int) -> None:
    ttl = max(int(exp_ts - datetime.now(timezone.utc).timestamp()), 1)
    await redis_client.setex(f"{BLACKLIST_PREFIX}{jti}", ttl, "1")


async def _is_blacklisted(jti: str) -> bool:
    return bool(await redis_client.exists(f"{BLACKLIST_PREFIX}{jti}"))


# ---------- user lookups ----------

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: uuid.UUID) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


# ---------- core flows ----------

async def authenticate(db: AsyncSession, email: str, password: str) -> User:
    user = await get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled",
        )
    return user


async def issue_token_pair(db: AsyncSession, user: User) -> TokenPair:
    access, _ = create_access_token(user.id)
    refresh, _ = create_refresh_token(user.id)

    user.last_login = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(user)

    return TokenPair(access_token=access, refresh_token=refresh, user=user)


async def refresh_access_token(db: AsyncSession, refresh_token: str) -> str:
    try:
        payload = decode_token(refresh_token)
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid refresh token") from e

    if payload.get("type") != REFRESH:
        raise HTTPException(status_code=401, detail="Wrong token type")

    jti = payload.get("jti")
    if jti and await _is_blacklisted(jti):
        raise HTTPException(status_code=401, detail="Refresh token revoked")

    user = await get_user_by_id(db, uuid.UUID(payload["sub"]))
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found")

    access, _ = create_access_token(user.id)
    return access


async def logout(token: str) -> None:
    """Blacklist the given access (or refresh) token until its natural exp."""
    try:
        payload = decode_token(token)
    except JWTError:
        return  # silent: nothing to revoke
    jti = payload.get("jti")
    exp = payload.get("exp")
    if jti and exp:
        await _blacklist_jti(jti, int(exp))


async def decode_access_token(token: str) -> dict:
    try:
        payload = decode_token(token)
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token") from e

    if payload.get("type") != ACCESS:
        raise HTTPException(status_code=401, detail="Wrong token type")

    jti = payload.get("jti")
    if jti and await _is_blacklisted(jti):
        raise HTTPException(status_code=401, detail="Token revoked")

    return payload


# ---------- bootstrap ----------

async def ensure_superadmin(db: AsyncSession) -> None:
    """Create initial superadmin from settings if not exists."""
    from app.models.user import Role

    existing = await get_user_by_email(db, settings.ADMIN_EMAIL)
    if existing:
        return
    user = User(
        email=settings.ADMIN_EMAIL,
        hashed_password=hash_password(settings.ADMIN_PASSWORD),
        full_name="Super Admin",
        role=Role.SUPERADMIN,
        is_active=True,
        is_verified=True,
    )
    db.add(user)
    await db.commit()
