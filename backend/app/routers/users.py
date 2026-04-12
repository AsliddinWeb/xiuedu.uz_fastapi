import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import Role, User
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.utils.deps import CurrentUser, require_roles
from app.utils.security import hash_password

router = APIRouter(prefix="/admin/users", tags=["admin:users"])
_su = require_roles(Role.SUPERADMIN)


@router.get("/", response_model=list[UserOut])
async def list_users(
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_su),
):
    rows = (await db.execute(select(User).order_by(User.created_at.desc()))).scalars().all()
    return rows


@router.post("/", response_model=UserOut, status_code=201)
async def create_user(
    payload: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_su),
):
    if (await db.execute(select(User).where(User.email == payload.email))).scalar_one_or_none():
        raise HTTPException(409, "Email already registered")
    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
        role=payload.role,
        is_active=payload.is_active,
        avatar_url=payload.avatar_url,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.put("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: uuid.UUID,
    payload: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_su),
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    data = payload.model_dump(exclude_unset=True)
    if "password" in data:
        user.hashed_password = hash_password(data.pop("password"))
    for k, v in data.items():
        setattr(user, k, v)
    await db.commit()
    await db.refresh(user)
    return user


@router.patch("/{user_id}/toggle-active", response_model=UserOut)
async def toggle_active(
    user_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current: User = Depends(_su),
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    if user.id == current.id:
        raise HTTPException(400, "Cannot deactivate yourself")
    user.is_active = not user.is_active
    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current: User = Depends(_su),
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    if user.id == current.id:
        raise HTTPException(400, "Cannot delete yourself")
    await db.delete(user)
    await db.commit()
