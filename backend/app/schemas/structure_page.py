from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ─────────────── StructurePage singleton ───────────────
class StructurePageBase(BaseModel):
    hero_eyebrow_uz: str | None = None
    hero_eyebrow_ru: str | None = None
    hero_eyebrow_en: str | None = None
    hero_title_uz: str | None = None
    hero_title_ru: str | None = None
    hero_title_en: str | None = None
    hero_subtitle_uz: str | None = None
    hero_subtitle_ru: str | None = None
    hero_subtitle_en: str | None = None

    top_eyebrow_uz: str | None = None
    top_eyebrow_ru: str | None = None
    top_eyebrow_en: str | None = None
    top_title_uz: str | None = None
    top_title_ru: str | None = None
    top_title_en: str | None = None

    academic_eyebrow_uz: str | None = None
    academic_eyebrow_ru: str | None = None
    academic_eyebrow_en: str | None = None
    academic_title_uz: str | None = None
    academic_title_ru: str | None = None
    academic_title_en: str | None = None
    academic_lead_uz: str | None = None
    academic_lead_ru: str | None = None
    academic_lead_en: str | None = None

    admin_eyebrow_uz: str | None = None
    admin_eyebrow_ru: str | None = None
    admin_eyebrow_en: str | None = None
    admin_title_uz: str | None = None
    admin_title_ru: str | None = None
    admin_title_en: str | None = None
    admin_lead_uz: str | None = None
    admin_lead_ru: str | None = None
    admin_lead_en: str | None = None

    services_eyebrow_uz: str | None = None
    services_eyebrow_ru: str | None = None
    services_eyebrow_en: str | None = None
    services_title_uz: str | None = None
    services_title_ru: str | None = None
    services_title_en: str | None = None
    services_lead_uz: str | None = None
    services_lead_ru: str | None = None
    services_lead_en: str | None = None

    cta_title_uz: str | None = None
    cta_title_ru: str | None = None
    cta_title_en: str | None = None
    cta_text_uz: str | None = None
    cta_text_ru: str | None = None
    cta_text_en: str | None = None
    cta_primary_label_uz: str | None = None
    cta_primary_label_ru: str | None = None
    cta_primary_label_en: str | None = None
    cta_primary_url: str | None = None
    cta_secondary_label_uz: str | None = None
    cta_secondary_label_ru: str | None = None
    cta_secondary_label_en: str | None = None
    cta_secondary_url: str | None = None


class StructurePageUpdate(StructurePageBase):
    pass


class StructurePageAdminOut(StructurePageBase, ORM):
    id: int
    updated_at: datetime


class StructurePagePublic(BaseModel):
    hero_eyebrow: str | None
    hero_title: str | None
    hero_subtitle: str | None

    top_eyebrow: str | None
    top_title: str | None

    academic_eyebrow: str | None
    academic_title: str | None
    academic_lead: str | None

    admin_eyebrow: str | None
    admin_title: str | None
    admin_lead: str | None

    services_eyebrow: str | None
    services_title: str | None
    services_lead: str | None

    cta_title: str | None
    cta_text: str | None
    cta_primary_label: str | None
    cta_primary_url: str | None
    cta_secondary_label: str | None
    cta_secondary_url: str | None


# ─────────────── AdminDepartment ───────────────
class AdminDepartmentBase(BaseModel):
    enabled: bool = True
    sort_order: int = 0
    icon: str
    name_uz: str
    name_ru: str
    name_en: str
    head_uz: str | None = None
    head_ru: str | None = None
    head_en: str | None = None
    email: str | None = None
    phone: str | None = None


class AdminDepartmentCreate(AdminDepartmentBase): pass


class AdminDepartmentUpdate(BaseModel):
    enabled: bool | None = None
    sort_order: int | None = None
    icon: str | None = None
    name_uz: str | None = None
    name_ru: str | None = None
    name_en: str | None = None
    head_uz: str | None = None
    head_ru: str | None = None
    head_en: str | None = None
    email: str | None = None
    phone: str | None = None


class AdminDepartmentAdminOut(AdminDepartmentBase, ORM):
    id: int


class AdminDepartmentPublic(BaseModel):
    id: int
    icon: str
    name: str
    head: str | None
    email: str | None
    phone: str | None


# ─────────────── SupportService ───────────────
class SupportServiceBase(BaseModel):
    enabled: bool = True
    sort_order: int = 0
    icon: str
    name_uz: str
    name_ru: str
    name_en: str
    desc_uz: str = ""
    desc_ru: str = ""
    desc_en: str = ""


class SupportServiceCreate(SupportServiceBase): pass


class SupportServiceUpdate(BaseModel):
    enabled: bool | None = None
    sort_order: int | None = None
    icon: str | None = None
    name_uz: str | None = None
    name_ru: str | None = None
    name_en: str | None = None
    desc_uz: str | None = None
    desc_ru: str | None = None
    desc_en: str | None = None


class SupportServiceAdminOut(SupportServiceBase, ORM):
    id: int


class SupportServicePublic(BaseModel):
    id: int
    icon: str
    name: str
    desc: str


# ─────────────── Aggregate ───────────────
# Includes references to leaders + faculties for the public view
class StructurePagePublicAggregate(BaseModel):
    page: StructurePagePublic | None
    rector: dict | None  # localized leader (rector group, first one)
    prorectors: list[dict]  # localized prorectors
    faculties: list[dict]   # minimal: id, slug, icon, name, programs_count
    departments: list[AdminDepartmentPublic]
    services: list[SupportServicePublic]
