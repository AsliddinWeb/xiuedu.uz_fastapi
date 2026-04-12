from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.media import MediaFile
from app.models.news import News
from app.models.page import StaticPage
from app.models.user import Role, User
from app.schemas.stats import ActivityItem, StatsOverview, TopNewsItem
from app.utils.deps import CurrentUser, require_roles
from app.utils.lang import pick

router = APIRouter(prefix="/admin/stats", tags=["admin:stats"])
_dep = require_roles(Role.ADMIN, Role.CONTENT_MANAGER)


@router.get("/overview", response_model=StatsOverview)
async def overview(
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    total_news = (await db.execute(select(func.count(News.id)))).scalar_one()
    published_news = (
        await db.execute(select(func.count(News.id)).where(News.is_published.is_(True)))
    ).scalar_one()
    total_pages = (await db.execute(select(func.count(StaticPage.id)))).scalar_one()
    published_pages = (
        await db.execute(
            select(func.count(StaticPage.id)).where(StaticPage.is_published.is_(True))
        )
    ).scalar_one()
    total_media = (await db.execute(select(func.count(MediaFile.id)))).scalar_one()
    total_media_size = (
        await db.execute(select(func.coalesce(func.sum(MediaFile.size_bytes), 0)))
    ).scalar_one()
    total_users = (await db.execute(select(func.count(User.id)))).scalar_one()

    views_total = (
        await db.execute(select(func.coalesce(func.sum(News.views_count), 0)))
    ).scalar_one()

    cutoff = datetime.now(timezone.utc) - timedelta(days=30)
    views_30d = (
        await db.execute(
            select(func.coalesce(func.sum(News.views_count), 0)).where(
                News.published_at.is_not(None), News.published_at >= cutoff
            )
        )
    ).scalar_one()

    top = (
        await db.execute(
            select(News).where(News.is_published.is_(True))
            .order_by(News.views_count.desc()).limit(5)
        )
    ).scalars().all()

    recent_news = (
        await db.execute(select(News).order_by(News.created_at.desc()).limit(5))
    ).scalars().all()
    recent_pages = (
        await db.execute(select(StaticPage).order_by(StaticPage.created_at.desc()).limit(5))
    ).scalars().all()
    recent_media = (
        await db.execute(select(MediaFile).order_by(MediaFile.created_at.desc()).limit(5))
    ).scalars().all()

    activity: list[ActivityItem] = []
    for n in recent_news:
        activity.append(ActivityItem(
            type="news", id=n.id, title=pick(n, "title", "uz") or n.slug, timestamp=n.created_at
        ))
    for p in recent_pages:
        activity.append(ActivityItem(
            type="page", id=p.id, title=pick(p, "title", "uz") or p.slug, timestamp=p.created_at
        ))
    for m in recent_media:
        activity.append(ActivityItem(
            type="media", id=m.id, title=m.original_name, timestamp=m.created_at
        ))
    activity.sort(key=lambda x: x.timestamp, reverse=True)
    activity = activity[:10]

    return StatsOverview(
        total_news=total_news,
        published_news=published_news,
        draft_news=total_news - published_news,
        total_pages=total_pages,
        published_pages=published_pages,
        total_media=total_media,
        total_media_size_bytes=int(total_media_size),
        total_users=total_users,
        news_views_total=int(views_total),
        news_views_30d=int(views_30d),
        top_news=[
            TopNewsItem(id=n.id, slug=n.slug, title=pick(n, "title", "uz") or n.slug, views_count=n.views_count)
            for n in top
        ],
        recent_activity=activity,
    )
