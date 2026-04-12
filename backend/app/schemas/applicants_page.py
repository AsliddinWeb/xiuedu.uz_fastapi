from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ─────────────── ApplicantsPage singleton ───────────────
class ApplicantsPageBase(BaseModel):
    hero_eyebrow_uz: str | None = None
    hero_eyebrow_ru: str | None = None
    hero_eyebrow_en: str | None = None
    hero_title_uz: str | None = None
    hero_title_ru: str | None = None
    hero_title_en: str | None = None
    hero_subtitle_uz: str | None = None
    hero_subtitle_ru: str | None = None
    hero_subtitle_en: str | None = None

    steps_eyebrow_uz: str | None = None
    steps_eyebrow_ru: str | None = None
    steps_eyebrow_en: str | None = None
    steps_title_uz: str | None = None
    steps_title_ru: str | None = None
    steps_title_en: str | None = None

    forms_eyebrow_uz: str | None = None
    forms_eyebrow_ru: str | None = None
    forms_eyebrow_en: str | None = None
    forms_title_uz: str | None = None
    forms_title_ru: str | None = None
    forms_title_en: str | None = None

    timeline_eyebrow_uz: str | None = None
    timeline_eyebrow_ru: str | None = None
    timeline_eyebrow_en: str | None = None
    timeline_title_uz: str | None = None
    timeline_title_ru: str | None = None
    timeline_title_en: str | None = None

    docs_eyebrow_uz: str | None = None
    docs_eyebrow_ru: str | None = None
    docs_eyebrow_en: str | None = None
    docs_title_uz: str | None = None
    docs_title_ru: str | None = None
    docs_title_en: str | None = None

    faq_eyebrow_uz: str | None = None
    faq_eyebrow_ru: str | None = None
    faq_eyebrow_en: str | None = None
    faq_title_uz: str | None = None
    faq_title_ru: str | None = None
    faq_title_en: str | None = None

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
    cta_primary_external: bool = True
    cta_phone_label: str | None = None
    cta_phone_url: str | None = None


class ApplicantsPageUpdate(ApplicantsPageBase):
    pass


class ApplicantsPageAdminOut(ApplicantsPageBase, ORM):
    id: int
    updated_at: datetime


class ApplicantsPagePublic(BaseModel):
    hero_eyebrow: str | None
    hero_title: str | None
    hero_subtitle: str | None
    steps_eyebrow: str | None
    steps_title: str | None
    forms_eyebrow: str | None
    forms_title: str | None
    timeline_eyebrow: str | None
    timeline_title: str | None
    docs_eyebrow: str | None
    docs_title: str | None
    faq_eyebrow: str | None
    faq_title: str | None
    cta_title: str | None
    cta_text: str | None
    cta_primary_label: str | None
    cta_primary_url: str | None
    cta_primary_external: bool
    cta_phone_label: str | None
    cta_phone_url: str | None


# ─────────────── Step ───────────────
class StepBase(BaseModel):
    enabled: bool = True
    sort_order: int = 0
    number: int
    icon: str
    title_uz: str
    title_ru: str
    title_en: str
    desc_uz: str = ""
    desc_ru: str = ""
    desc_en: str = ""


class StepCreate(StepBase): pass


class StepUpdate(BaseModel):
    enabled: bool | None = None
    sort_order: int | None = None
    number: int | None = None
    icon: str | None = None
    title_uz: str | None = None
    title_ru: str | None = None
    title_en: str | None = None
    desc_uz: str | None = None
    desc_ru: str | None = None
    desc_en: str | None = None


class StepAdminOut(StepBase, ORM):
    id: int


class StepPublic(BaseModel):
    id: int
    number: int
    icon: str
    title: str
    desc: str


# ─────────────── Form ───────────────
class FormBase(BaseModel):
    enabled: bool = True
    sort_order: int = 0
    title_uz: str
    title_ru: str
    title_en: str
    desc_uz: str = ""
    desc_ru: str = ""
    desc_en: str = ""
    features: list[dict] = []
    cta_label_uz: str | None = None
    cta_label_ru: str | None = None
    cta_label_en: str | None = None
    cta_url: str | None = None


class FormCreate(FormBase): pass


class FormUpdate(BaseModel):
    enabled: bool | None = None
    sort_order: int | None = None
    title_uz: str | None = None
    title_ru: str | None = None
    title_en: str | None = None
    desc_uz: str | None = None
    desc_ru: str | None = None
    desc_en: str | None = None
    features: list[dict] | None = None
    cta_label_uz: str | None = None
    cta_label_ru: str | None = None
    cta_label_en: str | None = None
    cta_url: str | None = None


class FormAdminOut(FormBase, ORM):
    id: int


class FormPublic(BaseModel):
    id: int
    title: str
    desc: str
    features: list[str]
    cta_label: str | None
    cta_url: str | None


# ─────────────── TimelineItem ───────────────
class TimelineBase(BaseModel):
    enabled: bool = True
    sort_order: int = 0
    month_uz: str
    month_ru: str
    month_en: str
    text_uz: str = ""
    text_ru: str = ""
    text_en: str = ""


class TimelineCreate(TimelineBase): pass


class TimelineUpdate(BaseModel):
    enabled: bool | None = None
    sort_order: int | None = None
    month_uz: str | None = None
    month_ru: str | None = None
    month_en: str | None = None
    text_uz: str | None = None
    text_ru: str | None = None
    text_en: str | None = None


class TimelineAdminOut(TimelineBase, ORM):
    id: int


class TimelinePublic(BaseModel):
    id: int
    month: str
    text: str


# ─────────────── DocCategory ───────────────
class DocBase(BaseModel):
    enabled: bool = True
    sort_order: int = 0
    title_uz: str
    title_ru: str
    title_en: str
    items: list[dict] = []


class DocCreate(DocBase): pass


class DocUpdate(BaseModel):
    enabled: bool | None = None
    sort_order: int | None = None
    title_uz: str | None = None
    title_ru: str | None = None
    title_en: str | None = None
    items: list[dict] | None = None


class DocAdminOut(DocBase, ORM):
    id: int


class DocPublic(BaseModel):
    id: int
    title: str
    items: list[str]


# ─────────────── FAQ ───────────────
class FaqBase(BaseModel):
    enabled: bool = True
    sort_order: int = 0
    question_uz: str
    question_ru: str
    question_en: str
    answer_uz: str
    answer_ru: str
    answer_en: str


class FaqCreate(FaqBase): pass


class FaqUpdate(BaseModel):
    enabled: bool | None = None
    sort_order: int | None = None
    question_uz: str | None = None
    question_ru: str | None = None
    question_en: str | None = None
    answer_uz: str | None = None
    answer_ru: str | None = None
    answer_en: str | None = None


class FaqAdminOut(FaqBase, ORM):
    id: int


class FaqPublic(BaseModel):
    id: int
    question: str
    answer: str


# ─────────────── Aggregate ───────────────
class ApplicantsPagePublicAggregate(BaseModel):
    page: ApplicantsPagePublic | None
    steps: list[StepPublic]
    forms: list[FormPublic]
    timeline: list[TimelinePublic]
    docs: list[DocPublic]
    faqs: list[FaqPublic]
