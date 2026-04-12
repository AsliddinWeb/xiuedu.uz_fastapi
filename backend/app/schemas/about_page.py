from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ──────────────── AboutPage (singleton) ────────────────
class AboutPageBase(BaseModel):
    hero_eyebrow_uz: str | None = None
    hero_eyebrow_ru: str | None = None
    hero_eyebrow_en: str | None = None
    hero_title_uz: str | None = None
    hero_title_ru: str | None = None
    hero_title_en: str | None = None
    hero_subtitle_uz: str | None = None
    hero_subtitle_ru: str | None = None
    hero_subtitle_en: str | None = None

    rector_image: str | None = None
    rector_name_uz: str | None = None
    rector_name_ru: str | None = None
    rector_name_en: str | None = None
    rector_role_uz: str | None = None
    rector_role_ru: str | None = None
    rector_role_en: str | None = None
    rector_degree_uz: str | None = None
    rector_degree_ru: str | None = None
    rector_degree_en: str | None = None

    rector_letter_eyebrow_uz: str | None = None
    rector_letter_eyebrow_ru: str | None = None
    rector_letter_eyebrow_en: str | None = None
    rector_letter_title_uz: str | None = None
    rector_letter_title_ru: str | None = None
    rector_letter_title_en: str | None = None
    rector_letter_paragraphs: list[dict] = []

    mvv_eyebrow_uz: str | None = None
    mvv_eyebrow_ru: str | None = None
    mvv_eyebrow_en: str | None = None
    mvv_title_uz: str | None = None
    mvv_title_ru: str | None = None
    mvv_title_en: str | None = None
    mission_uz: str | None = None
    mission_ru: str | None = None
    mission_en: str | None = None
    vision_uz: str | None = None
    vision_ru: str | None = None
    vision_en: str | None = None
    values_uz: str | None = None
    values_ru: str | None = None
    values_en: str | None = None

    address_uz: str | None = None
    address_ru: str | None = None
    address_en: str | None = None
    contact_email: str | None = None
    map_embed_url: str | None = None


class AboutPageUpdate(AboutPageBase):
    pass


class AboutPageAdminOut(AboutPageBase, ORM):
    id: int
    updated_at: datetime


class AboutPagePublic(BaseModel):
    """Localized AboutPage payload."""
    hero_eyebrow: str | None
    hero_title: str | None
    hero_subtitle: str | None

    rector_image: str | None
    rector_name: str | None
    rector_role: str | None
    rector_degree: str | None

    rector_letter_eyebrow: str | None
    rector_letter_title: str | None
    rector_letter_paragraphs: list[str]

    mvv_eyebrow: str | None
    mvv_title: str | None
    mission: str | None
    vision: str | None
    values: str | None

    address: str | None
    contact_email: str | None
    map_embed_url: str | None


# ──────────────── Timeline ────────────────
class TimelineEventBase(BaseModel):
    enabled: bool = True
    sort_order: int = 0
    year: str
    title_uz: str
    title_ru: str
    title_en: str
    text_uz: str = ""
    text_ru: str = ""
    text_en: str = ""


class TimelineEventCreate(TimelineEventBase):
    pass


class TimelineEventUpdate(BaseModel):
    enabled: bool | None = None
    sort_order: int | None = None
    year: str | None = None
    title_uz: str | None = None
    title_ru: str | None = None
    title_en: str | None = None
    text_uz: str | None = None
    text_ru: str | None = None
    text_en: str | None = None


class TimelineEventAdminOut(TimelineEventBase, ORM):
    id: int


class TimelineEventPublicOut(BaseModel):
    id: int
    year: str
    title: str
    text: str


# ──────────────── Accreditation ────────────────
class AccreditationBase(BaseModel):
    enabled: bool = True
    sort_order: int = 0
    code: str
    icon: str = "ShieldCheckIcon"
    name_uz: str
    name_ru: str
    name_en: str


class AccreditationCreate(AccreditationBase):
    pass


class AccreditationUpdate(BaseModel):
    enabled: bool | None = None
    sort_order: int | None = None
    code: str | None = None
    icon: str | None = None
    name_uz: str | None = None
    name_ru: str | None = None
    name_en: str | None = None


class AccreditationAdminOut(AccreditationBase, ORM):
    id: int


class AccreditationPublicOut(BaseModel):
    id: int
    code: str
    icon: str
    name: str


# ──────────────── Aggregate ────────────────
class AboutPagePublicAggregate(BaseModel):
    page: AboutPagePublic | None
    timeline: list[TimelineEventPublicOut]
    accreditations: list[AccreditationPublicOut]
