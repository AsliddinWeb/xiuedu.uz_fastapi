from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ─────────────── InternationalPage singleton ───────────────
class IntlPageBase(BaseModel):
    hero_eyebrow_uz: str | None = None
    hero_eyebrow_ru: str | None = None
    hero_eyebrow_en: str | None = None
    hero_title_uz: str | None = None
    hero_title_ru: str | None = None
    hero_title_en: str | None = None
    hero_subtitle_uz: str | None = None
    hero_subtitle_ru: str | None = None
    hero_subtitle_en: str | None = None

    stat1_value: str | None = None
    stat1_label_uz: str | None = None
    stat1_label_ru: str | None = None
    stat1_label_en: str | None = None
    stat2_value: str | None = None
    stat2_label_uz: str | None = None
    stat2_label_ru: str | None = None
    stat2_label_en: str | None = None
    stat3_value: str | None = None
    stat3_label_uz: str | None = None
    stat3_label_ru: str | None = None
    stat3_label_en: str | None = None
    stat4_value: str | None = None
    stat4_label_uz: str | None = None
    stat4_label_ru: str | None = None
    stat4_label_en: str | None = None

    programs_eyebrow_uz: str | None = None
    programs_eyebrow_ru: str | None = None
    programs_eyebrow_en: str | None = None
    programs_title_uz: str | None = None
    programs_title_ru: str | None = None
    programs_title_en: str | None = None

    partners_eyebrow_uz: str | None = None
    partners_eyebrow_ru: str | None = None
    partners_eyebrow_en: str | None = None
    partners_title_uz: str | None = None
    partners_title_ru: str | None = None
    partners_title_en: str | None = None

    cta_title_uz: str | None = None
    cta_title_ru: str | None = None
    cta_title_en: str | None = None
    cta_text_uz: str | None = None
    cta_text_ru: str | None = None
    cta_text_en: str | None = None
    cta_email: str | None = None
    cta_phone_label: str | None = None
    cta_phone_url: str | None = None


class IntlPageUpdate(IntlPageBase):
    pass


class IntlPageAdminOut(IntlPageBase, ORM):
    id: int
    updated_at: datetime


class IntlStat(BaseModel):
    value: str | None
    label: str | None


class IntlPagePublic(BaseModel):
    hero_eyebrow: str | None
    hero_title: str | None
    hero_subtitle: str | None

    stats: list[IntlStat]

    programs_eyebrow: str | None
    programs_title: str | None
    partners_eyebrow: str | None
    partners_title: str | None

    cta_title: str | None
    cta_text: str | None
    cta_email: str | None
    cta_phone_label: str | None
    cta_phone_url: str | None


# ─────────────── IntlProgram ───────────────
class IntlProgramBase(BaseModel):
    enabled: bool = True
    sort_order: int = 0
    icon: str
    title_uz: str
    title_ru: str
    title_en: str
    desc_uz: str = ""
    desc_ru: str = ""
    desc_en: str = ""


class IntlProgramCreate(IntlProgramBase): pass


class IntlProgramUpdate(BaseModel):
    enabled: bool | None = None
    sort_order: int | None = None
    icon: str | None = None
    title_uz: str | None = None
    title_ru: str | None = None
    title_en: str | None = None
    desc_uz: str | None = None
    desc_ru: str | None = None
    desc_en: str | None = None


class IntlProgramAdminOut(IntlProgramBase, ORM):
    id: int


class IntlProgramPublic(BaseModel):
    id: int
    icon: str
    title: str
    desc: str


# ─────────────── IntlPartner ───────────────
class IntlPartnerBase(BaseModel):
    enabled: bool = True
    sort_order: int = 0
    name: str
    country_code: str = ""
    flag: str = ""
    logo_url: str | None = None
    url: str | None = None


class IntlPartnerCreate(IntlPartnerBase): pass


class IntlPartnerUpdate(BaseModel):
    enabled: bool | None = None
    sort_order: int | None = None
    name: str | None = None
    country_code: str | None = None
    flag: str | None = None
    logo_url: str | None = None
    url: str | None = None


class IntlPartnerAdminOut(IntlPartnerBase, ORM):
    id: int


class IntlPartnerPublic(BaseModel):
    id: int
    name: str
    country_code: str
    flag: str
    logo_url: str | None
    url: str | None


# ─────────────── Aggregate ───────────────
class IntlPagePublicAggregate(BaseModel):
    page: IntlPagePublic | None
    programs: list[IntlProgramPublic]
    partners: list[IntlPartnerPublic]
