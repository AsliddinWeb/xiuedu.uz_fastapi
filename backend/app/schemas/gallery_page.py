from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ─── GalleryPage singleton ───
class GalleryPageBase(BaseModel):
    hero_eyebrow_uz: str | None = None
    hero_eyebrow_ru: str | None = None
    hero_eyebrow_en: str | None = None
    hero_title_uz: str | None = None
    hero_title_ru: str | None = None
    hero_title_en: str | None = None
    hero_subtitle_uz: str | None = None
    hero_subtitle_ru: str | None = None
    hero_subtitle_en: str | None = None


class GalleryPageUpdate(GalleryPageBase): pass


class GalleryPageAdminOut(GalleryPageBase, ORM):
    id: int
    updated_at: datetime


class GalleryPagePublic(BaseModel):
    hero_eyebrow: str | None
    hero_title: str | None
    hero_subtitle: str | None


# ─── GalleryCategory ───
class GalleryCategoryBase(BaseModel):
    enabled: bool = True
    sort_order: int = 0
    slug: str
    name_uz: str
    name_ru: str
    name_en: str


class GalleryCategoryCreate(GalleryCategoryBase): pass


class GalleryCategoryUpdate(BaseModel):
    enabled: bool | None = None
    sort_order: int | None = None
    slug: str | None = None
    name_uz: str | None = None
    name_ru: str | None = None
    name_en: str | None = None


class GalleryCategoryAdminOut(GalleryCategoryBase, ORM):
    id: int


class GalleryCategoryPublic(BaseModel):
    id: int
    slug: str
    name: str


# ─── GalleryItem ───
class GalleryItemBase(BaseModel):
    enabled: bool = True
    sort_order: int = 0
    image: str
    caption_uz: str = ""
    caption_ru: str = ""
    caption_en: str = ""
    alt_uz: str = ""
    alt_ru: str = ""
    alt_en: str = ""


class GalleryItemCreate(GalleryItemBase):
    category_id: int


class GalleryItemUpdate(BaseModel):
    enabled: bool | None = None
    sort_order: int | None = None
    category_id: int | None = None
    image: str | None = None
    caption_uz: str | None = None
    caption_ru: str | None = None
    caption_en: str | None = None
    alt_uz: str | None = None
    alt_ru: str | None = None
    alt_en: str | None = None


class GalleryItemAdminOut(GalleryItemBase, ORM):
    id: int
    category_id: int


class GalleryItemPublic(BaseModel):
    id: int
    image: str
    caption: str
    alt: str
    category_slug: str


# ─── Aggregate ───
class GalleryPagePublicAggregate(BaseModel):
    page: GalleryPagePublic | None
    categories: list[GalleryCategoryPublic]
    items: list[GalleryItemPublic]
