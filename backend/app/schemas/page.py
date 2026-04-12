import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StaticPageBase(BaseModel):
    slug: str
    is_published: bool = True
    page_order: int = 0
    parent_id: int | None = None

    title_uz: str
    title_ru: str
    title_en: str

    content_uz: str = ""
    content_ru: str = ""
    content_en: str = ""

    meta_title_uz: str | None = None
    meta_title_ru: str | None = None
    meta_title_en: str | None = None
    meta_description_uz: str | None = None
    meta_description_ru: str | None = None
    meta_description_en: str | None = None
    og_image: str | None = None


class StaticPageCreate(StaticPageBase):
    pass


class StaticPageUpdate(BaseModel):
    slug: str | None = None
    is_published: bool | None = None
    page_order: int | None = None
    parent_id: int | None = None

    title_uz: str | None = None
    title_ru: str | None = None
    title_en: str | None = None
    content_uz: str | None = None
    content_ru: str | None = None
    content_en: str | None = None

    meta_title_uz: str | None = None
    meta_title_ru: str | None = None
    meta_title_en: str | None = None
    meta_description_uz: str | None = None
    meta_description_ru: str | None = None
    meta_description_en: str | None = None
    og_image: str | None = None


class StaticPageAdminOut(StaticPageBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_by: uuid.UUID | None
    created_at: datetime
    updated_at: datetime


class StaticPagePublicOut(BaseModel):
    """Localized public payload."""
    id: int
    slug: str
    title: str
    content: str
    meta_title: str | None
    meta_description: str | None
    og_image: str | None
    parent_id: int | None
    page_order: int
    updated_at: datetime


class StaticPageNavItem(BaseModel):
    id: int
    slug: str
    title: str
    parent_id: int | None
    page_order: int
