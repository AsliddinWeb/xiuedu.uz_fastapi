from datetime import date, datetime
from pydantic import BaseModel, ConfigDict


class ORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ─────────────── VacanciesPage singleton ───────────────
class VacanciesPageBase(BaseModel):
    hero_eyebrow_uz: str | None = None
    hero_eyebrow_ru: str | None = None
    hero_eyebrow_en: str | None = None
    hero_title_uz: str | None = None
    hero_title_ru: str | None = None
    hero_title_en: str | None = None
    hero_subtitle_uz: str | None = None
    hero_subtitle_ru: str | None = None
    hero_subtitle_en: str | None = None

    empty_title_uz: str | None = None
    empty_title_ru: str | None = None
    empty_title_en: str | None = None
    empty_text_uz: str | None = None
    empty_text_ru: str | None = None
    empty_text_en: str | None = None

    cv_title_uz: str | None = None
    cv_title_ru: str | None = None
    cv_title_en: str | None = None
    cv_text_uz: str | None = None
    cv_text_ru: str | None = None
    cv_text_en: str | None = None
    cv_email: str | None = None


class VacanciesPageUpdate(VacanciesPageBase):
    pass


class VacanciesPageAdminOut(VacanciesPageBase, ORM):
    id: int
    updated_at: datetime


class VacanciesPagePublic(BaseModel):
    hero_eyebrow: str | None
    hero_title: str | None
    hero_subtitle: str | None
    empty_title: str | None
    empty_text: str | None
    cv_title: str | None
    cv_text: str | None
    cv_email: str | None


# ─────────────── Vacancy ───────────────
class VacancyBase(BaseModel):
    enabled: bool = True
    sort_order: int = 0
    is_open: bool = True
    title_uz: str
    title_ru: str
    title_en: str
    department_uz: str = ""
    department_ru: str = ""
    department_en: str = ""
    employment_type: str = "full_time"  # full_time | part_time | contract | internship | online
    location_uz: str = ""
    location_ru: str = ""
    location_en: str = ""
    description_uz: str = ""
    description_ru: str = ""
    description_en: str = ""
    requirements_uz: str = ""
    requirements_ru: str = ""
    requirements_en: str = ""
    salary: str | None = None
    contact_email: str | None = None
    apply_url: str | None = None
    posted_at: date | None = None
    deadline: date | None = None


class VacancyCreate(VacancyBase): pass


class VacancyUpdate(BaseModel):
    enabled: bool | None = None
    sort_order: int | None = None
    is_open: bool | None = None
    title_uz: str | None = None
    title_ru: str | None = None
    title_en: str | None = None
    department_uz: str | None = None
    department_ru: str | None = None
    department_en: str | None = None
    employment_type: str | None = None
    location_uz: str | None = None
    location_ru: str | None = None
    location_en: str | None = None
    description_uz: str | None = None
    description_ru: str | None = None
    description_en: str | None = None
    requirements_uz: str | None = None
    requirements_ru: str | None = None
    requirements_en: str | None = None
    salary: str | None = None
    contact_email: str | None = None
    apply_url: str | None = None
    posted_at: date | None = None
    deadline: date | None = None


class VacancyAdminOut(VacancyBase, ORM):
    id: int
    created_at: datetime
    updated_at: datetime


class VacancyPublic(BaseModel):
    id: int
    is_open: bool
    title: str
    department: str
    employment_type: str
    location: str
    description: str
    requirements: str
    salary: str | None
    contact_email: str | None
    apply_url: str | None
    posted_at: date | None
    deadline: date | None


# ─────────────── Aggregate ───────────────
class VacanciesPagePublicAggregate(BaseModel):
    page: VacanciesPagePublic | None
    vacancies: list[VacancyPublic]
    departments: list[str]  # unique department names for filter
