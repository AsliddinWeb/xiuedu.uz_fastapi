"""Gallery page routes — public aggregate + admin CRUD."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.gallery_page import GalleryPage, GalleryCategory, GalleryItem
from app.models.user import Role, User
from app.schemas.gallery_page import (
    GalleryPageAdminOut, GalleryPagePublic, GalleryPagePublicAggregate, GalleryPageUpdate,
    GalleryCategoryAdminOut, GalleryCategoryCreate, GalleryCategoryPublic, GalleryCategoryUpdate,
    GalleryItemAdminOut, GalleryItemCreate, GalleryItemPublic, GalleryItemUpdate,
)
from app.utils.deps import require_roles
from app.utils.lang import Lang, get_lang, pick

# ── Public ──
public = APIRouter(prefix="/page-settings", tags=["page-settings:gallery"])


@public.get("/gallery", response_model=GalleryPagePublicAggregate)
async def get_gallery(
    db: Annotated[AsyncSession, Depends(get_db)],
    lang: Annotated[Lang, Depends(get_lang)],
):
    page = (await db.execute(select(GalleryPage).limit(1))).scalar_one_or_none()
    cats = (await db.execute(
        select(GalleryCategory).where(GalleryCategory.enabled.is_(True))
                               .options(selectinload(GalleryCategory.items))
                               .order_by(GalleryCategory.sort_order, GalleryCategory.id)
    )).scalars().all()

    cat_slug_map = {c.id: c.slug for c in cats}
    all_items = []
    for c in cats:
        for item in c.items:
            if not item.enabled:
                continue
            all_items.append(GalleryItemPublic(
                id=item.id,
                image=item.image,
                caption=pick(item, "caption", lang) or "",
                alt=pick(item, "alt", lang) or "",
                category_slug=cat_slug_map.get(item.category_id, ""),
            ))

    return GalleryPagePublicAggregate(
        page=GalleryPagePublic(
            hero_eyebrow=pick(page, "hero_eyebrow", lang) if page else None,
            hero_title=pick(page, "hero_title", lang) if page else None,
            hero_subtitle=pick(page, "hero_subtitle", lang) if page else None,
        ) if page else None,
        categories=[
            GalleryCategoryPublic(
                id=c.id, slug=c.slug,
                name=pick(c, "name", lang) or "",
            ) for c in cats
        ],
        items=all_items,
    )


# ── Admin ──
admin = APIRouter(prefix="/admin/gallery", tags=["admin:gallery"])
_dep = require_roles(Role.ADMIN, Role.CONTENT_MANAGER)


# Page singleton
@admin.get("/page", response_model=GalleryPageAdminOut)
async def admin_get_page(
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    p = (await db.execute(select(GalleryPage).limit(1))).scalar_one_or_none()
    if not p:
        p = GalleryPage()
        db.add(p); await db.commit(); await db.refresh(p)
    return p


@admin.put("/page", response_model=GalleryPageAdminOut)
async def admin_update_page(
    payload: GalleryPageUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    p = (await db.execute(select(GalleryPage).limit(1))).scalar_one_or_none()
    if not p:
        p = GalleryPage(); db.add(p)
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(p, k, v)
    await db.commit(); await db.refresh(p)
    return p


# Categories CRUD
@admin.get("/categories", response_model=list[GalleryCategoryAdminOut])
async def admin_list_cats(
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    return (await db.execute(
        select(GalleryCategory).order_by(GalleryCategory.sort_order, GalleryCategory.id)
    )).scalars().all()


@admin.post("/categories", response_model=GalleryCategoryAdminOut, status_code=201)
async def admin_create_cat(
    payload: GalleryCategoryCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    if (await db.execute(select(GalleryCategory).where(GalleryCategory.slug == payload.slug))).scalar_one_or_none():
        raise HTTPException(409, "Slug already exists")
    obj = GalleryCategory(**payload.model_dump())
    db.add(obj); await db.commit(); await db.refresh(obj)
    return obj


@admin.put("/categories/{item_id}", response_model=GalleryCategoryAdminOut)
async def admin_update_cat(
    item_id: int, payload: GalleryCategoryUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    obj = await db.get(GalleryCategory, item_id)
    if not obj: raise HTTPException(404, "Not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.commit(); await db.refresh(obj)
    return obj


@admin.delete("/categories/{item_id}", status_code=204)
async def admin_delete_cat(
    item_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    obj = await db.get(GalleryCategory, item_id)
    if not obj: raise HTTPException(404, "Not found")
    await db.delete(obj); await db.commit()


# Items CRUD
@admin.get("/items", response_model=list[GalleryItemAdminOut])
async def admin_list_items(
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    return (await db.execute(
        select(GalleryItem).order_by(GalleryItem.sort_order, GalleryItem.id.desc())
    )).scalars().all()


@admin.post("/items", response_model=GalleryItemAdminOut, status_code=201)
async def admin_create_item(
    payload: GalleryItemCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    if not await db.get(GalleryCategory, payload.category_id):
        raise HTTPException(404, "Category not found")
    obj = GalleryItem(**payload.model_dump())
    db.add(obj); await db.commit(); await db.refresh(obj)
    return obj


@admin.put("/items/{item_id}", response_model=GalleryItemAdminOut)
async def admin_update_item(
    item_id: int, payload: GalleryItemUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    obj = await db.get(GalleryItem, item_id)
    if not obj: raise HTTPException(404, "Not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.commit(); await db.refresh(obj)
    return obj


@admin.delete("/items/{item_id}", status_code=204)
async def admin_delete_item(
    item_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    obj = await db.get(GalleryItem, item_id)
    if not obj: raise HTTPException(404, "Not found")
    await db.delete(obj); await db.commit()
