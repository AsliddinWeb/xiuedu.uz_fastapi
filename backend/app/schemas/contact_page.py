from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ContactPageBase(BaseModel):
    hero_eyebrow_uz: str | None = None
    hero_eyebrow_ru: str | None = None
    hero_eyebrow_en: str | None = None
    hero_title_uz: str | None = None
    hero_title_ru: str | None = None
    hero_title_en: str | None = None
    hero_subtitle_uz: str | None = None
    hero_subtitle_ru: str | None = None
    hero_subtitle_en: str | None = None

    address_uz: str | None = None
    address_ru: str | None = None
    address_en: str | None = None
    phone: str | None = None
    email: str | None = None
    working_hours_uz: str | None = None
    working_hours_ru: str | None = None
    working_hours_en: str | None = None

    form_title_uz: str | None = None
    form_title_ru: str | None = None
    form_title_en: str | None = None
    form_subtitle_uz: str | None = None
    form_subtitle_ru: str | None = None
    form_subtitle_en: str | None = None

    map_embed_url: str | None = None


class ContactPageUpdate(ContactPageBase):
    pass


class ContactPageAdminOut(ContactPageBase, ORM):
    id: int
    updated_at: datetime


class ContactPagePublic(BaseModel):
    hero_eyebrow: str | None
    hero_title: str | None
    hero_subtitle: str | None

    address: str | None
    phone: str | None
    email: str | None
    working_hours: str | None

    form_title: str | None
    form_subtitle: str | None

    map_embed_url: str | None
