import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# ===== Categories =====

class CategoryBase(BaseModel):
    slug: str
    name_uz: str
    name_ru: str
    name_en: str
    color: str | None = None
    icon: str | None = None
    is_active: bool = True
    sort_order: int = 0


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    slug: str | None = None
    name_uz: str | None = None
    name_ru: str | None = None
    name_en: str | None = None
    color: str | None = None
    icon: str | None = None
    is_active: bool | None = None
    sort_order: int | None = None


class CategoryAdminOut(CategoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class CategoryPublicOut(BaseModel):
    id: int
    slug: str
    name: str
    color: str | None
    icon: str | None


# ===== News =====

class NewsBase(BaseModel):
    slug: str
    title_uz: str
    title_ru: str
    title_en: str
    excerpt_uz: str = ""
    excerpt_ru: str = ""
    excerpt_en: str = ""
    body_uz: str = ""
    body_ru: str = ""
    body_en: str = ""
    cover_image: str | None = None
    gallery: list[str] = Field(default_factory=list)
    is_published: bool = False
    is_featured: bool = False
    category_id: int | None = None
    published_at: datetime | None = None

    meta_title_uz: str | None = None
    meta_title_ru: str | None = None
    meta_title_en: str | None = None
    meta_description_uz: str | None = None
    meta_description_ru: str | None = None
    meta_description_en: str | None = None


class NewsCreate(NewsBase):
    pass


class NewsUpdate(BaseModel):
    slug: str | None = None
    title_uz: str | None = None
    title_ru: str | None = None
    title_en: str | None = None
    excerpt_uz: str | None = None
    excerpt_ru: str | None = None
    excerpt_en: str | None = None
    body_uz: str | None = None
    body_ru: str | None = None
    body_en: str | None = None
    cover_image: str | None = None
    gallery: list[str] | None = None
    is_published: bool | None = None
    is_featured: bool | None = None
    category_id: int | None = None
    published_at: datetime | None = None

    meta_title_uz: str | None = None
    meta_title_ru: str | None = None
    meta_title_en: str | None = None
    meta_description_uz: str | None = None
    meta_description_ru: str | None = None
    meta_description_en: str | None = None


class NewsAdminOut(NewsBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    views_count: int
    author_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime


class NewsPublicListItem(BaseModel):
    id: int
    slug: str
    title: str
    excerpt: str
    cover_image: str | None
    is_featured: bool
    views_count: int
    published_at: datetime | None
    category: CategoryPublicOut | None


class NewsPublicDetail(BaseModel):
    id: int
    slug: str
    title: str
    excerpt: str
    body: str
    cover_image: str | None
    gallery: list[str]
    views_count: int
    published_at: datetime | None
    meta_title: str | None
    meta_description: str | None
    category: CategoryPublicOut | None


class NewsStats(BaseModel):
    total: int
    published: int
    draft: int
    featured: int
    total_views: int
