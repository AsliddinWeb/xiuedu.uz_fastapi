import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EventBase(BaseModel):
    slug: str
    title_uz: str
    title_ru: str
    title_en: str
    description_uz: str = ""
    description_ru: str = ""
    description_en: str = ""

    starts_at: datetime
    ends_at: datetime | None = None
    location_uz: str = ""
    location_ru: str = ""
    location_en: str = ""

    cover_image: str | None = None
    gallery: list[str] = Field(default_factory=list)

    is_published: bool = False
    is_featured: bool = False

    meta_title_uz: str | None = None
    meta_title_ru: str | None = None
    meta_title_en: str | None = None
    meta_description_uz: str | None = None
    meta_description_ru: str | None = None
    meta_description_en: str | None = None


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    slug: str | None = None
    title_uz: str | None = None
    title_ru: str | None = None
    title_en: str | None = None
    description_uz: str | None = None
    description_ru: str | None = None
    description_en: str | None = None

    starts_at: datetime | None = None
    ends_at: datetime | None = None
    location_uz: str | None = None
    location_ru: str | None = None
    location_en: str | None = None

    cover_image: str | None = None
    gallery: list[str] | None = None

    is_published: bool | None = None
    is_featured: bool | None = None


class EventAdminOut(EventBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    author_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime


class EventPublicListItem(BaseModel):
    id: int
    slug: str
    title: str
    description: str
    location: str
    cover_image: str | None
    is_featured: bool
    starts_at: datetime
    ends_at: datetime | None


class EventPublicDetail(BaseModel):
    id: int
    slug: str
    title: str
    description: str
    location: str
    cover_image: str | None
    gallery: list[str]
    starts_at: datetime
    ends_at: datetime | None
    meta_title: str | None
    meta_description: str | None
