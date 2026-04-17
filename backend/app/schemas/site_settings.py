from datetime import datetime
from pydantic import BaseModel, ConfigDict


class SiteSettingsBase(BaseModel):
    site_name_uz: str | None = None
    site_name_ru: str | None = None
    site_name_en: str | None = None
    site_short_name: str | None = None

    logo_url: str | None = None
    logo_dark_url: str | None = None
    favicon_url: str | None = None
    og_image_url: str | None = None

    footer_desc_uz: str | None = None
    footer_desc_ru: str | None = None
    footer_desc_en: str | None = None

    telegram_url: str | None = None
    instagram_url: str | None = None
    facebook_url: str | None = None
    youtube_url: str | None = None

    phone: str | None = None
    email: str | None = None
    address_uz: str | None = None
    address_ru: str | None = None
    address_en: str | None = None

    hemis_url: str | None = None
    admission_url: str | None = None

    google_analytics_id: str | None = None
    yandex_metrica_id: str | None = None


class SiteSettingsUpdate(SiteSettingsBase):
    pass


class SiteSettingsAdminOut(SiteSettingsBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    updated_at: datetime


class SiteSettingsPublic(BaseModel):
    site_name: str | None
    site_short_name: str | None
    logo_url: str | None
    logo_dark_url: str | None
    favicon_url: str | None
    og_image_url: str | None
    footer_desc: str | None

    telegram_url: str | None
    instagram_url: str | None
    facebook_url: str | None
    youtube_url: str | None

    phone: str | None
    email: str | None
    address: str | None

    hemis_url: str | None
    admission_url: str | None
