from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.auth import AccessToken, LoginRequest, RefreshRequest, TokenPair
from app.schemas.user import PasswordChange, ProfileUpdate, UserOut
from app.services import auth_service
from app.utils.deps import CurrentUser
from app.utils.security import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenPair)
async def login(
    payload: LoginRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    user = await auth_service.authenticate(db, payload.email, payload.password)
    return await auth_service.issue_token_pair(db, user)


@router.post("/refresh", response_model=AccessToken)
async def refresh(
    payload: RefreshRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    access = await auth_service.refresh_access_token(db, payload.refresh_token)
    return AccessToken(access_token=access)


@router.post("/logout", status_code=204)
async def logout(
    request: Request,
    authorization: Annotated[str | None, Header()] = None,
    _: CurrentUser = None,  # type: ignore[assignment]
):
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1]
        await auth_service.logout(token)
    return None


@router.get("/me", response_model=UserOut)
async def me(current: CurrentUser):
    return current


@router.patch("/me", response_model=UserOut)
async def update_me(
    payload: ProfileUpdate,
    current: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    for k, v in payload.model_dump(exclude_unset=True).items():
        if v is not None:
            setattr(current, k, v)
    await db.commit()
    await db.refresh(current)
    return current


@router.post("/me/password", status_code=204)
async def change_my_password(
    payload: PasswordChange,
    current: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    if not verify_password(payload.current_password, current.hashed_password):
        raise HTTPException(400, "Current password is incorrect")
    if len(payload.new_password) < 8:
        raise HTTPException(400, "New password must be at least 8 characters")
    current.hashed_password = hash_password(payload.new_password)
    await db.commit()
    return None
