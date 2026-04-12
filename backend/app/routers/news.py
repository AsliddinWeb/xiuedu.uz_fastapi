from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.middleware.cache import invalidate
from app.models.news import News, NewsCategory
from app.models.user import User, Role
from app.schemas.common import Paginated
from app.schemas.news import (
    CategoryAdminOut,
    CategoryCreate,
    CategoryPublicOut,
    CategoryUpdate,
    NewsAdminOut,
    NewsCreate,
    NewsPublicDetail,
    NewsPublicListItem,
    NewsStats,
    NewsUpdate,
)
from app.utils.deps import CurrentUser, require_roles
from app.utils.lang import Lang, get_lang, pick
from app.utils.seo import fill_news_seo

# ===== Public router =====
public = APIRouter(prefix="/news", tags=["news"])


def _cat_public(c: NewsCategory | None, lang: Lang) -> CategoryPublicOut | None:
    if not c:
        return None
    return CategoryPublicOut(
        id=c.id,
        slug=c.slug,
        name=pick(c, "name", lang) or "",
        color=c.color,
        icon=c.icon,
    )


def _list_item(n: News, lang: Lang) -> NewsPublicListItem:
    return NewsPublicListItem(
        id=n.id,
        slug=n.slug,
        title=pick(n, "title", lang) or "",
        excerpt=pick(n, "excerpt", lang) or "",
        cover_image=n.cover_image,
        is_featured=n.is_featured,
        views_count=n.views_count,
        published_at=n.published_at,
        category=_cat_public(n.category, lang),
    )


def _detail(n: News, lang: Lang) -> NewsPublicDetail:
    return NewsPublicDetail(
        id=n.id,
        slug=n.slug,
        title=pick(n, "title", lang) or "",
        excerpt=pick(n, "excerpt", lang) or "",
        body=pick(n, "body", lang) or "",
        cover_image=n.cover_image,
        gallery=n.gallery or [],
        views_count=n.views_count,
        published_at=n.published_at,
        meta_title=pick(n, "meta_title", lang),
        meta_description=pick(n, "meta_description", lang),
        category=_cat_public(n.category, lang),
    )


@public.get("/", response_model=Paginated[NewsPublicListItem])
async def list_news(
    db: Annotated[AsyncSession, Depends(get_db)],
    lang: Annotated[Lang, Depends(get_lang)],
    page: int = Query(1, ge=1),
    limit: int = Query(12, ge=1, le=100),
    category: str | None = Query(None, description="category slug"),
    featured: bool | None = Query(None),
):
    stmt = select(News).where(News.is_published.is_(True)).options(selectinload(News.category))
    if category:
        stmt = stmt.join(NewsCategory).where(NewsCategory.slug == category)
    if featured is not None:
        stmt = stmt.where(News.is_featured.is_(featured))

    total = (await db.execute(select(func.count()).select_from(stmt.subquery()))).scalar_one()
    rows = (
        await db.execute(
            stmt.order_by(News.published_at.desc().nulls_last(), News.id.desc())
            .offset((page - 1) * limit)
            .limit(limit)
        )
    ).scalars().all()

    return Paginated[NewsPublicListItem](
        items=[_list_item(n, lang) for n in rows],
        total=total,
        page=page,
        limit=limit,
        pages=(total + limit - 1) // limit,
    )


@public.get("/categories/", response_model=list[CategoryPublicOut])
async def list_categories(
    db: Annotated[AsyncSession, Depends(get_db)],
    lang: Annotated[Lang, Depends(get_lang)],
):
    rows = (
        await db.execute(
            select(NewsCategory)
            .where(NewsCategory.is_active.is_(True))
            .order_by(NewsCategory.sort_order, NewsCategory.id)
        )
    ).scalars().all()
    return [_cat_public(c, lang) for c in rows]


@public.get("/{slug}", response_model=NewsPublicDetail)
async def get_news_detail(
    slug: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    lang: Annotated[Lang, Depends(get_lang)],
):
    n = (
        await db.execute(
            select(News)
            .where(News.slug == slug, News.is_published.is_(True))
            .options(selectinload(News.category))
        )
    ).scalar_one_or_none()
    if not n:
        raise HTTPException(404, "News not found")
    n.views_count = (n.views_count or 0) + 1
    await db.commit()
    await db.refresh(n)
    return _detail(n, lang)


# ===== Admin: Categories =====
admin_cat = APIRouter(prefix="/admin/news/categories", tags=["admin:categories"])
_cm = require_roles(Role.ADMIN, Role.CONTENT_MANAGER)


@admin_cat.get("/", response_model=list[CategoryAdminOut])
async def admin_list_categories(
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_cm),
):
    rows = (
        await db.execute(select(NewsCategory).order_by(NewsCategory.sort_order, NewsCategory.id))
    ).scalars().all()
    return rows


@admin_cat.post("/", response_model=CategoryAdminOut, status_code=201)
async def admin_create_category(
    payload: CategoryCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_cm),
):
    if (await db.execute(select(NewsCategory).where(NewsCategory.slug == payload.slug))).scalar_one_or_none():
        raise HTTPException(409, "Slug already exists")
    c = NewsCategory(**payload.model_dump())
    db.add(c)
    await db.commit()
    await db.refresh(c)
    return c


@admin_cat.put("/{cat_id}", response_model=CategoryAdminOut)
async def admin_update_category(
    cat_id: int,
    payload: CategoryUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_cm),
):
    c = await db.get(NewsCategory, cat_id)
    if not c:
        raise HTTPException(404, "Category not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(c, k, v)
    await db.commit()
    await db.refresh(c)
    return c


@admin_cat.delete("/{cat_id}", status_code=204)
async def admin_delete_category(
    cat_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_cm),
):
    c = await db.get(NewsCategory, cat_id)
    if not c:
        raise HTTPException(404, "Category not found")
    await db.delete(c)
    await db.commit()


# ===== Admin: News =====
admin_news = APIRouter(prefix="/admin/news", tags=["admin:news"])


@admin_news.get("/stats", response_model=NewsStats)
async def admin_news_stats(
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_cm),
):
    total = (await db.execute(select(func.count(News.id)))).scalar_one()
    published = (
        await db.execute(select(func.count(News.id)).where(News.is_published.is_(True)))
    ).scalar_one()
    featured = (
        await db.execute(select(func.count(News.id)).where(News.is_featured.is_(True)))
    ).scalar_one()
    total_views = (await db.execute(select(func.coalesce(func.sum(News.views_count), 0)))).scalar_one()
    return NewsStats(
        total=total,
        published=published,
        draft=total - published,
        featured=featured,
        total_views=int(total_views),
    )


@admin_news.get("/", response_model=Paginated[NewsAdminOut])
async def admin_list_news(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=200),
    _u: User = Depends(_cm),
):
    total = (await db.execute(select(func.count(News.id)))).scalar_one()
    rows = (
        await db.execute(
            select(News).order_by(News.id.desc()).offset((page - 1) * limit).limit(limit)
        )
    ).scalars().all()
    return Paginated[NewsAdminOut](
        items=rows,
        total=total,
        page=page,
        limit=limit,
        pages=(total + limit - 1) // limit,
    )


@admin_news.post("/", response_model=NewsAdminOut, status_code=201)
async def admin_create_news(
    payload: NewsCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: User = Depends(_cm),
):
    if (await db.execute(select(News).where(News.slug == payload.slug))).scalar_one_or_none():
        raise HTTPException(409, "Slug already exists")
    data = payload.model_dump()
    if data.get("is_published") and not data.get("published_at"):
        data["published_at"] = datetime.now(timezone.utc)
    fill_news_seo(data)
    n = News(**data, author_id=user.id)
    db.add(n)
    await db.commit()
    await db.refresh(n)
    await invalidate("news")
    return n


@admin_news.put("/{news_id}", response_model=NewsAdminOut)
async def admin_update_news(
    news_id: int,
    payload: NewsUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_cm),
):
    n = await db.get(News, news_id)
    if not n:
        raise HTTPException(404, "News not found")
    update_data = payload.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(n, k, v)
    # Re-derive SEO from current content (always overwrite — keeps meta in sync).
    seo_payload = {
        f: getattr(n, f) for f in (
            "title_uz", "title_ru", "title_en",
            "excerpt_uz", "excerpt_ru", "excerpt_en",
            "body_uz", "body_ru", "body_en",
        )
    }
    fill_news_seo(seo_payload)
    for lang in ("uz", "ru", "en"):
        setattr(n, f"meta_title_{lang}", seo_payload.get(f"meta_title_{lang}"))
        setattr(n, f"meta_description_{lang}", seo_payload.get(f"meta_description_{lang}"))
    if n.is_published and not n.published_at:
        n.published_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(n)
    await invalidate("news")
    return n


@admin_news.delete("/{news_id}", status_code=204)
async def admin_delete_news(
    news_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_cm),
):
    n = await db.get(News, news_id)
    if not n:
        raise HTTPException(404, "News not found")
    await db.delete(n)
    await db.commit()
    await invalidate("news")


@admin_news.patch("/{news_id}/publish", response_model=NewsAdminOut)
async def admin_publish_news(
    news_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    publish: bool = Query(True),
    _u: User = Depends(_cm),
):
    n = await db.get(News, news_id)
    if not n:
        raise HTTPException(404, "News not found")
    n.is_published = publish
    if publish and not n.published_at:
        n.published_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(n)
    await invalidate("news")
    return n
