from datetime import datetime

from pydantic import BaseModel


class TopNewsItem(BaseModel):
    id: int
    slug: str
    title: str
    views_count: int


class ActivityItem(BaseModel):
    type: str           # "news" | "page" | "media"
    id: int
    title: str
    timestamp: datetime


class StatsOverview(BaseModel):
    total_news: int
    published_news: int
    draft_news: int
    total_pages: int
    published_pages: int
    total_media: int
    total_media_size_bytes: int
    total_users: int
    news_views_total: int
    news_views_30d: int
    top_news: list[TopNewsItem]
    recent_activity: list[ActivityItem]
