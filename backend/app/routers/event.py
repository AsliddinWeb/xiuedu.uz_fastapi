from datetime import datetime, timezone
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.cache import invalidate
from app.models.event import Event
from app.models.user import Role, User
from app.schemas.common import Paginated
from app.schemas.event import (
    EventAdminOut, EventCreate, EventPublicDetail, EventPublicListItem, EventUpdate
)
from app.utils.deps import CurrentUser, require_roles
from app.utils.lang import Lang, get_lang, pick
from app.utils.seo import fill_event_seo

# ===== Public router =====
public = APIRouter(prefix="/events", tags=["events"])


def _list_item(e: Event, lang: Lang) -> EventPublicListItem:
    return EventPublicListItem(
        id=e.id,
        slug=e.slug,
        title=pick(e, "title", lang) or "",
        description=pick(e, "description", lang) or "",
        location=pick(e, "location", lang) or "",
        cover_image=e.cover_image,
        is_featured=e.is_featured,
        starts_at=e.starts_at,
        ends_at=e.ends_at,
    )


def _detail(e: Event, lang: Lang) -> EventPublicDetail:
    return EventPublicDetail(
        id=e.id,
        slug=e.slug,
        title=pick(e, "title", lang) or "",
        description=pick(e, "description", lang) or "",
        location=pick(e, "location", lang) or "",
        cover_image=e.cover_image,
        gallery=e.gallery or [],
        starts_at=e.starts_at,
        ends_at=e.ends_at,
        meta_title=pick(e, "meta_title", lang),
        meta_description=pick(e, "meta_description", lang),
    )


@public.get("/", response_model=Paginated[EventPublicListItem])
async def list_events(
    db: Annotated[AsyncSession, Depends(get_db)],
    lang: Annotated[Lang, Depends(get_lang)],
    page: int = Query(1, ge=1),
    limit: int = Query(12, ge=1, le=100),
    when: Literal["upcoming", "past", "all"] = Query("upcoming"),
):
    now = datetime.now(timezone.utc)
    stmt = select(Event).where(Event.is_published.is_(True))
    if when == "upcoming":
        stmt = stmt.where(Event.starts_at >= now).order_by(Event.starts_at.asc())
    elif when == "past":
        stmt = stmt.where(Event.starts_at < now).order_by(Event.starts_at.desc())
    else:
        stmt = stmt.order_by(Event.starts_at.desc())

    total = (await db.execute(select(func.count()).select_from(stmt.subquery()))).scalar_one()
    rows = (
        await db.execute(stmt.offset((page - 1) * limit).limit(limit))
    ).scalars().all()

    return Paginated[EventPublicListItem](
        items=[_list_item(e, lang) for e in rows],
        total=total,
        page=page,
        limit=limit,
        pages=(total + limit - 1) // limit,
    )


@public.get("/{slug}", response_model=EventPublicDetail)
async def get_event(
    slug: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    lang: Annotated[Lang, Depends(get_lang)],
):
    e = (
        await db.execute(
            select(Event).where(Event.slug == slug, Event.is_published.is_(True))
        )
    ).scalar_one_or_none()
    if not e:
        raise HTTPException(404, "Event not found")
    return _detail(e, lang)


# ===== Admin router =====
admin = APIRouter(prefix="/admin/events", tags=["admin:events"])
_dep = require_roles(Role.ADMIN, Role.CONTENT_MANAGER)


@admin.get("/", response_model=Paginated[EventAdminOut])
async def admin_list_events(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=200),
    _u: User = Depends(_dep),
):
    total = (await db.execute(select(func.count(Event.id)))).scalar_one()
    rows = (
        await db.execute(
            select(Event).order_by(Event.starts_at.desc()).offset((page - 1) * limit).limit(limit)
        )
    ).scalars().all()
    return Paginated[EventAdminOut](
        items=rows,
        total=total,
        page=page,
        limit=limit,
        pages=(total + limit - 1) // limit,
    )


@admin.get("/{event_id}", response_model=EventAdminOut)
async def admin_get_event(
    event_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    e = await db.get(Event, event_id)
    if not e:
        raise HTTPException(404, "Event not found")
    return e


@admin.post("/", response_model=EventAdminOut, status_code=201)
async def admin_create_event(
    payload: EventCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: User = Depends(_dep),
):
    if (await db.execute(select(Event).where(Event.slug == payload.slug))).scalar_one_or_none():
        raise HTTPException(409, "Slug already exists")
    data = payload.model_dump()
    fill_event_seo(data)
    e = Event(**data, author_id=user.id)
    db.add(e)
    await db.commit()
    await db.refresh(e)
    await invalidate("events")
    return e


@admin.put("/{event_id}", response_model=EventAdminOut)
async def admin_update_event(
    event_id: int,
    payload: EventUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    e = await db.get(Event, event_id)
    if not e:
        raise HTTPException(404, "Event not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(e, k, v)
    seo_payload = {
        f: getattr(e, f) for f in (
            "title_uz", "title_ru", "title_en",
            "description_uz", "description_ru", "description_en",
        )
    }
    fill_event_seo(seo_payload)
    for lang in ("uz", "ru", "en"):
        setattr(e, f"meta_title_{lang}", seo_payload.get(f"meta_title_{lang}"))
        setattr(e, f"meta_description_{lang}", seo_payload.get(f"meta_description_{lang}"))
    await db.commit()
    await db.refresh(e)
    await invalidate("events")
    return e


@admin.delete("/{event_id}", status_code=204)
async def admin_delete_event(
    event_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    e = await db.get(Event, event_id)
    if not e:
        raise HTTPException(404, "Event not found")
    await db.delete(e)
    await db.commit()
    await invalidate("events")
