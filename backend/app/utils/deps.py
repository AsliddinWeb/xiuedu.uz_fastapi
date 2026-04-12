import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import Role, User
from app.services.auth_service import decode_access_token, get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


async def get_current_user(
    token: Annotated[str | None, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = await decode_access_token(token)
    try:
        user_id = uuid.UUID(payload["sub"])
    except (KeyError, ValueError) as e:
        raise HTTPException(status_code=401, detail="Invalid token subject") from e

    user = await get_user_by_id(db, user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    return user


def require_roles(*allowed: Role):
    async def checker(
        current: Annotated[User, Depends(get_current_user)],
    ) -> User:
        if current.role not in allowed and current.role != Role.SUPERADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current

    return checker


CurrentUser = Annotated[User, Depends(get_current_user)]
