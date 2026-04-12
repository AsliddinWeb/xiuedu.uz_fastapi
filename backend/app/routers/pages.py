from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.cache import invalidate
from app.models.page import StaticPage
from app.models.user import User, Role
from app.schemas.page import (
    StaticPageAdminOut,
    StaticPageCreate,
    StaticPageNavItem,
    StaticPagePublicOut,
    StaticPageUpdate,
)
from app.utils.deps import CurrentUser, require_roles
from app.utils.lang import Lang, get_lang, pick
from app.utils.seo import fill_page_seo

# ===== Public router =====
public = APIRouter(prefix="/pages", tags=["pages"])


def _to_public(page: StaticPage, lang: Lang) -> StaticPagePublicOut:
    return StaticPagePublicOut(
        id=page.id,
        slug=page.slug,
        title=pick(page, "title", lang) or "",
        content=pick(page, "content", lang) or "",
        meta_title=pick(page, "meta_title", lang),
        meta_description=pick(page, "meta_description", lang),
        og_image=page.og_image,
        parent_id=page.parent_id,
        page_order=page.page_order,
        updated_at=page.updated_at,
    )


@public.get("/", response_model=list[StaticPageNavItem])
async def list_published_pages(
    db: Annotated[AsyncSession, Depends(get_db)],
    lang: Annotated[Lang, Depends(get_lang)],
):
    rows = (
        await db.execute(
            select(StaticPage)
            .where(StaticPage.is_published.is_(True))
            .order_by(StaticPage.page_order, StaticPage.id)
        )
    ).scalars().all()
    return [
        StaticPageNavItem(
            id=p.id,
            slug=p.slug,
            title=pick(p, "title", lang) or "",
            parent_id=p.parent_id,
            page_order=p.page_order,
        )
        for p in rows
    ]


@public.get("/{slug}", response_model=StaticPagePublicOut)
async def get_page_by_slug(
    slug: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    lang: Annotated[Lang, Depends(get_lang)],
):
    page = (
        await db.execute(
            select(StaticPage).where(
                StaticPage.slug == slug, StaticPage.is_published.is_(True)
            )
        )
    ).scalar_one_or_none()
    if not page:
        raise HTTPException(404, "Page not found")
    return _to_public(page, lang)


# ===== Admin router =====
admin = APIRouter(prefix="/admin/pages", tags=["admin:pages"])

_admin_dep = require_roles(Role.ADMIN, Role.PAGE_EDITOR)


@admin.get("/", response_model=list[StaticPageAdminOut])
async def admin_list_pages(
    db: Annotated[AsyncSession, Depends(get_db)],
    _user: User = Depends(_admin_dep),
):
    rows = (
        await db.execute(select(StaticPage).order_by(StaticPage.page_order, StaticPage.id))
    ).scalars().all()
    return rows


@admin.post("/", response_model=StaticPageAdminOut, status_code=201)
async def admin_create_page(
    payload: StaticPageCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: User = Depends(_admin_dep),
):
    exists = (
        await db.execute(select(StaticPage).where(StaticPage.slug == payload.slug))
    ).scalar_one_or_none()
    if exists:
        raise HTTPException(409, "Slug already exists")
    data = payload.model_dump()
    fill_page_seo(data)
    page = StaticPage(**data, created_by=user.id)
    db.add(page)
    await db.commit()
    await db.refresh(page)
    await invalidate("page")
    return page


@admin.put("/{page_id}", response_model=StaticPageAdminOut)
async def admin_update_page(
    page_id: int,
    payload: StaticPageUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _user: User = Depends(_admin_dep),
):
    page = await db.get(StaticPage, page_id)
    if not page:
        raise HTTPException(404, "Page not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(page, k, v)
    seo_payload = {
        f: getattr(page, f) for f in (
            "title_uz", "title_ru", "title_en",
            "content_uz", "content_ru", "content_en",
        )
    }
    fill_page_seo(seo_payload)
    for lang in ("uz", "ru", "en"):
        setattr(page, f"meta_title_{lang}", seo_payload.get(f"meta_title_{lang}"))
        setattr(page, f"meta_description_{lang}", seo_payload.get(f"meta_description_{lang}"))
    await db.commit()
    await db.refresh(page)
    await invalidate("page")
    return page


@admin.delete("/{page_id}", status_code=204)
async def admin_delete_page(
    page_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _user: User = Depends(_admin_dep),
):
    page = await db.get(StaticPage, page_id)
    if not page:
        raise HTTPException(404, "Page not found")
    await db.delete(page)
    await db.commit()
    await invalidate("page")


@admin.patch("/{page_id}/publish", response_model=StaticPageAdminOut)
async def admin_toggle_publish(
    page_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    publish: bool = Query(True),
    _user: User = Depends(_admin_dep),
):
    page = await db.get(StaticPage, page_id)
    if not page:
        raise HTTPException(404, "Page not found")
    page.is_published = publish
    await db.commit()
    await db.refresh(page)
    await invalidate("page")
    return page
