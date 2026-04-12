"""
Leadership routes — public lang-aware list and admin CRUD.
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.leader import Leader
from app.models.user import Role, User
from app.schemas.leader import (
    LeaderAdminOut, LeaderCreate, LeaderPublicOut, LeaderUpdate,
)
from app.utils.deps import require_roles
from app.utils.lang import Lang, get_lang, pick

# ─────────────────────────────────────────────────────────────────
#  Public
# ─────────────────────────────────────────────────────────────────
public = APIRouter(prefix="/leaders", tags=["leaders"])


def _to_public(l: Leader, lang: Lang) -> LeaderPublicOut:
    return LeaderPublicOut(
        id=l.id,
        group=l.group,
        name=pick(l, "name", lang) or "",
        position=pick(l, "position", lang) or "",
        degree=pick(l, "degree", lang) or "",
        bio=pick(l, "bio", lang) or "",
        photo=l.photo,
        email=l.email,
        phone=l.phone,
    )


@public.get("/", response_model=list[LeaderPublicOut])
async def list_leaders(
    db: Annotated[AsyncSession, Depends(get_db)],
    lang: Annotated[Lang, Depends(get_lang)],
):
    rows = (await db.execute(
        select(Leader).where(Leader.enabled.is_(True))
                      .order_by(Leader.sort_order, Leader.id)
    )).scalars().all()
    return [_to_public(l, lang) for l in rows]


# ─────────────────────────────────────────────────────────────────
#  Admin
# ─────────────────────────────────────────────────────────────────
admin = APIRouter(prefix="/admin/leaders", tags=["admin:leaders"])
_dep = require_roles(Role.ADMIN, Role.CONTENT_MANAGER)


@admin.get("/", response_model=list[LeaderAdminOut])
async def admin_list(
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    rows = (await db.execute(
        select(Leader).order_by(Leader.sort_order, Leader.id)
    )).scalars().all()
    return rows


@admin.get("/{leader_id}", response_model=LeaderAdminOut)
async def admin_get(
    leader_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    obj = await db.get(Leader, leader_id)
    if not obj:
        raise HTTPException(404, "Not found")
    return obj


@admin.post("/", response_model=LeaderAdminOut, status_code=201)
async def admin_create(
    payload: LeaderCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    obj = Leader(**payload.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@admin.put("/{leader_id}", response_model=LeaderAdminOut)
async def admin_update(
    leader_id: int,
    payload: LeaderUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    obj = await db.get(Leader, leader_id)
    if not obj:
        raise HTTPException(404, "Not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.commit()
    await db.refresh(obj)
    return obj


@admin.delete("/{leader_id}", status_code=204)
async def admin_delete(
    leader_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    obj = await db.get(Leader, leader_id)
    if not obj:
        raise HTTPException(404, "Not found")
    await db.delete(obj)
    await db.commit()
