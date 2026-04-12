"""
Pydantic schemas for the home page CMS.

Two flavours per resource:
  * AdminOut / Create / Update — full multilingual fields, used by admin UI.
  * PublicOut / PublicAggregate — already localized to one language, used
    by public HomeView.
"""
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


# ──────────────────────────────────────────────────────────
#  Mixins / helpers
# ──────────────────────────────────────────────────────────
class ORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ══════════════════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════════════════
class HeroBase(BaseModel):
    variant: str = "split"
    enabled: bool = True

    eyebrow_uz: str | None = None
    eyebrow_ru: str | None = None
    eyebrow_en: str | None = None

    title_uz: str | None = None
    title_ru: str | None = None
    title_en: str | None = None

    title_highlight_uz: str | None = None
    title_highlight_ru: str | None = None
    title_highlight_en: str | None = None

    title_tail_uz: str | None = None
    title_tail_ru: str | None = None
    title_tail_en: str | None = None

    subtitle_uz: str | None = None
    subtitle_ru: str | None = None
    subtitle_en: str | None = None

    bg_image: str | None = None
    bg_video: str | None = None
    bg_video_poster: str | None = None
    side_image: str | None = None
    overlay_opacity: int = 55

    cta_primary_label_uz: str | None = None
    cta_primary_label_ru: str | None = None
    cta_primary_label_en: str | None = None
    cta_primary_url: str | None = None
    cta_primary_external: bool = False

    cta_secondary_label_uz: str | None = None
    cta_secondary_label_ru: str | None = None
    cta_secondary_label_en: str | None = None
    cta_secondary_url: str | None = None
    cta_secondary_external: bool = False

    show_particles: bool = True
    show_scroll_indicator: bool = True
    show_trust_badges: bool = True
    show_floating_cards: bool = True

    quote_text_uz: str | None = None
    quote_text_ru: str | None = None
    quote_text_en: str | None = None
    quote_author_uz: str | None = None
    quote_author_ru: str | None = None
    quote_author_en: str | None = None


class HeroUpdate(HeroBase):
    pass


class HeroAdminOut(HeroBase, ORM):
    id: int
    page: str
    updated_at: datetime


class HeroPublicOut(BaseModel):
    """Localized hero for public HomeView."""
    variant: str
    enabled: bool

    eyebrow: str | None
    title: str | None
    title_highlight: str | None
    title_tail: str | None
    subtitle: str | None

    bg_image: str | None
    bg_video: str | None
    bg_video_poster: str | None
    side_image: str | None
    overlay_opacity: int

    cta_primary_label: str | None
    cta_primary_url: str | None
    cta_primary_external: bool

    cta_secondary_label: str | None
    cta_secondary_url: str | None
    cta_secondary_external: bool

    show_particles: bool
    show_scroll_indicator: bool
    show_trust_badges: bool
    show_floating_cards: bool

    quote_text: str | None
    quote_author: str | None


# ══════════════════════════════════════════════════════════
#  HOME SECTION
# ══════════════════════════════════════════════════════════
class SectionBase(BaseModel):
    enabled: bool = True
    sort_order: int = 0
    eyebrow_uz: str | None = None
    eyebrow_ru: str | None = None
    eyebrow_en: str | None = None
    title_uz: str | None = None
    title_ru: str | None = None
    title_en: str | None = None
    subtitle_uz: str | None = None
    subtitle_ru: str | None = None
    subtitle_en: str | None = None
    settings: dict = {}


class SectionUpdate(SectionBase):
    pass


class SectionAdminOut(SectionBase, ORM):
    id: int
    key: str
    updated_at: datetime


class SectionPublicOut(BaseModel):
    key: str
    enabled: bool
    sort_order: int
    eyebrow: str | None
    title: str | None
    subtitle: str | None
    settings: dict


# ══════════════════════════════════════════════════════════
#  QUICK ACTION
# ══════════════════════════════════════════════════════════
class QuickActionBase(BaseModel):
    enabled: bool = True
    sort_order: int = 0
    icon: str
    title_uz: str
    title_ru: str
    title_en: str
    desc_uz: str = ""
    desc_ru: str = ""
    desc_en: str = ""
    url: str
    external: bool = False
    accent: bool = False


class QuickActionCreate(QuickActionBase):
    pass


class QuickActionUpdate(BaseModel):
    enabled: bool | None = None
    sort_order: int | None = None
    icon: str | None = None
    title_uz: str | None = None
    title_ru: str | None = None
    title_en: str | None = None
    desc_uz: str | None = None
    desc_ru: str | None = None
    desc_en: str | None = None
    url: str | None = None
    external: bool | None = None
    accent: bool | None = None


class QuickActionAdminOut(QuickActionBase, ORM):
    id: int


class QuickActionPublicOut(BaseModel):
    id: int
    icon: str
    title: str
    desc: str
    url: str
    external: bool
    accent: bool


# ══════════════════════════════════════════════════════════
#  INTRO PILLAR
# ══════════════════════════════════════════════════════════
class IntroPillarBase(BaseModel):
    enabled: bool = True
    sort_order: int = 0
    icon: str
    title_uz: str
    title_ru: str
    title_en: str
    desc_uz: str = ""
    desc_ru: str = ""
    desc_en: str = ""


class IntroPillarCreate(IntroPillarBase):
    pass


class IntroPillarUpdate(BaseModel):
    enabled: bool | None = None
    sort_order: int | None = None
    icon: str | None = None
    title_uz: str | None = None
    title_ru: str | None = None
    title_en: str | None = None
    desc_uz: str | None = None
    desc_ru: str | None = None
    desc_en: str | None = None


class IntroPillarAdminOut(IntroPillarBase, ORM):
    id: int


class IntroPillarPublicOut(BaseModel):
    id: int
    icon: str
    title: str
    desc: str


# ══════════════════════════════════════════════════════════
#  CAMPUS (singleton)
# ══════════════════════════════════════════════════════════
class CampusBase(BaseModel):
    main_image: str | None = None
    image_2: str | None = None
    image_3: str | None = None
    video_url: str | None = None
    eyebrow_uz: str | None = None
    eyebrow_ru: str | None = None
    eyebrow_en: str | None = None
    title_uz: str | None = None
    title_ru: str | None = None
    title_en: str | None = None
    text_uz: str | None = None
    text_ru: str | None = None
    text_en: str | None = None
    bullets: list[dict] = []
    cta_label_uz: str | None = None
    cta_label_ru: str | None = None
    cta_label_en: str | None = None
    cta_url: str | None = None


class CampusUpdate(CampusBase):
    pass


class CampusAdminOut(CampusBase, ORM):
    id: int
    updated_at: datetime


class CampusPublicOut(BaseModel):
    main_image: str | None
    image_2: str | None
    image_3: str | None
    video_url: str | None
    eyebrow: str | None
    title: str | None
    text: str | None
    bullets: list[str]
    cta_label: str | None
    cta_url: str | None


# ══════════════════════════════════════════════════════════
#  WHY CARD
# ══════════════════════════════════════════════════════════
class WhyCardBase(BaseModel):
    enabled: bool = True
    sort_order: int = 0
    icon: str
    icon_bg: str = "bg-primary-50"
    icon_color: str = "text-primary-700"
    number: str = ""
    number_label_uz: str = ""
    number_label_ru: str = ""
    number_label_en: str = ""
    title_uz: str
    title_ru: str
    title_en: str
    desc_uz: str = ""
    desc_ru: str = ""
    desc_en: str = ""


class WhyCardCreate(WhyCardBase):
    pass


class WhyCardUpdate(BaseModel):
    enabled: bool | None = None
    sort_order: int | None = None
    icon: str | None = None
    icon_bg: str | None = None
    icon_color: str | None = None
    number: str | None = None
    number_label_uz: str | None = None
    number_label_ru: str | None = None
    number_label_en: str | None = None
    title_uz: str | None = None
    title_ru: str | None = None
    title_en: str | None = None
    desc_uz: str | None = None
    desc_ru: str | None = None
    desc_en: str | None = None


class WhyCardAdminOut(WhyCardBase, ORM):
    id: int


class WhyCardPublicOut(BaseModel):
    id: int
    icon: str
    icon_bg: str
    icon_color: str
    number: str
    number_label: str
    title: str
    desc: str


# ══════════════════════════════════════════════════════════
#  FACULTY + PROGRAM
# ══════════════════════════════════════════════════════════
class StudyFormItem(BaseModel):
    form: str = "full_time"
    tuition: str = ""
    seats: int | None = None


class FacultyProgramBase(BaseModel):
    enabled: bool = True
    sort_order: int = 0
    level: str = "bachelor"          # bachelor | master | short | phd
    study_form: str = "full_time"    # legacy — kept for compat
    study_forms: list[StudyFormItem] = []  # NEW: multiple forms with per-form tuition
    name_uz: str
    name_ru: str
    name_en: str
    icon: str
    bg_class: str = "bg-indigo-50"
    icon_bg_class: str = "bg-indigo-500"
    ring_class: str = "ring-indigo-200/60"
    duration_uz: str = ""
    duration_ru: str = ""
    duration_en: str = ""
    tuition: str = ""                # legacy — primary tuition
    language_uz: str = ""
    language_ru: str = ""
    language_en: str = ""
    degree_uz: str = ""
    degree_ru: str = ""
    degree_en: str = ""
    credits: int | None = None
    seats: int | None = None         # legacy — total seats


class FacultyProgramCreate(FacultyProgramBase):
    pass


class FacultyProgramUpdate(BaseModel):
    enabled: bool | None = None
    sort_order: int | None = None
    level: str | None = None
    study_form: str | None = None
    name_uz: str | None = None
    name_ru: str | None = None
    name_en: str | None = None
    icon: str | None = None
    bg_class: str | None = None
    icon_bg_class: str | None = None
    ring_class: str | None = None
    duration_uz: str | None = None
    duration_ru: str | None = None
    duration_en: str | None = None
    tuition: str | None = None
    language_uz: str | None = None
    language_ru: str | None = None
    language_en: str | None = None
    degree_uz: str | None = None
    degree_ru: str | None = None
    degree_en: str | None = None
    credits: int | None = None
    seats: int | None = None


class FacultyProgramAdminOut(FacultyProgramBase, ORM):
    id: int
    faculty_id: int


class StudyFormOut(BaseModel):
    form: str        # full_time | part_time | evening | online
    tuition: str
    seats: int | None = None


class FacultyProgramPublicOut(BaseModel):
    id: int
    level: str
    study_forms: list[StudyFormOut]
    name: str
    icon: str
    bg_class: str
    icon_bg_class: str
    ring_class: str
    duration: str
    language: str
    degree: str
    credits: int | None


class FacultyBase(BaseModel):
    enabled: bool = True
    sort_order: int = 0
    slug: str
    icon: str
    name_uz: str
    name_ru: str
    name_en: str
    description_uz: str = ""
    description_ru: str = ""
    description_en: str = ""
    cover_image: str | None = None


class FacultyCreate(FacultyBase):
    pass


class FacultyUpdate(BaseModel):
    enabled: bool | None = None
    sort_order: int | None = None
    slug: str | None = None
    icon: str | None = None
    name_uz: str | None = None
    name_ru: str | None = None
    name_en: str | None = None
    description_uz: str | None = None
    description_ru: str | None = None
    description_en: str | None = None
    cover_image: str | None = None


class FacultyAdminOut(FacultyBase, ORM):
    id: int
    programs: list[FacultyProgramAdminOut] = []
    created_at: datetime
    updated_at: datetime


class FacultyPublicOut(BaseModel):
    id: int
    slug: str
    icon: str
    name: str
    description: str
    cover_image: str | None
    programs: list[FacultyProgramPublicOut]


# ══════════════════════════════════════════════════════════
#  ADMISSION STEP
# ══════════════════════════════════════════════════════════
class AdmissionStepBase(BaseModel):
    enabled: bool = True
    sort_order: int = 0
    number: str
    icon: str
    title_uz: str
    title_ru: str
    title_en: str
    desc_uz: str = ""
    desc_ru: str = ""
    desc_en: str = ""


class AdmissionStepCreate(AdmissionStepBase):
    pass


class AdmissionStepUpdate(BaseModel):
    enabled: bool | None = None
    sort_order: int | None = None
    number: str | None = None
    icon: str | None = None
    title_uz: str | None = None
    title_ru: str | None = None
    title_en: str | None = None
    desc_uz: str | None = None
    desc_ru: str | None = None
    desc_en: str | None = None


class AdmissionStepAdminOut(AdmissionStepBase, ORM):
    id: int


class AdmissionStepPublicOut(BaseModel):
    id: int
    number: str
    icon: str
    title: str
    desc: str


# ══════════════════════════════════════════════════════════
#  STAT
# ══════════════════════════════════════════════════════════
class StatBase(BaseModel):
    enabled: bool = True
    sort_order: int = 0
    value: str
    label_uz: str
    label_ru: str
    label_en: str
    sub_uz: str = ""
    sub_ru: str = ""
    sub_en: str = ""


class StatCreate(StatBase):
    pass


class StatUpdate(BaseModel):
    enabled: bool | None = None
    sort_order: int | None = None
    value: str | None = None
    label_uz: str | None = None
    label_ru: str | None = None
    label_en: str | None = None
    sub_uz: str | None = None
    sub_ru: str | None = None
    sub_en: str | None = None


class StatAdminOut(StatBase, ORM):
    id: int


class StatPublicOut(BaseModel):
    id: int
    value: str
    label: str
    sub: str


# ══════════════════════════════════════════════════════════
#  TESTIMONIAL
# ══════════════════════════════════════════════════════════
class TestimonialBase(BaseModel):
    enabled: bool = True
    sort_order: int = 0
    name_uz: str
    name_ru: str
    name_en: str
    role_uz: str = ""
    role_ru: str = ""
    role_en: str = ""
    text_uz: str
    text_ru: str
    text_en: str
    avatar: str | None = None
    rating: int = 5
    year: int | None = None


class TestimonialCreate(TestimonialBase):
    pass


class TestimonialUpdate(BaseModel):
    enabled: bool | None = None
    sort_order: int | None = None
    name_uz: str | None = None
    name_ru: str | None = None
    name_en: str | None = None
    role_uz: str | None = None
    role_ru: str | None = None
    role_en: str | None = None
    text_uz: str | None = None
    text_ru: str | None = None
    text_en: str | None = None
    avatar: str | None = None
    rating: int | None = None
    year: int | None = None


class TestimonialAdminOut(TestimonialBase, ORM):
    id: int


class TestimonialPublicOut(BaseModel):
    id: int
    name: str
    role: str
    text: str
    avatar: str | None
    rating: int
    year: int | None


# ══════════════════════════════════════════════════════════
#  PARTNER
# ══════════════════════════════════════════════════════════
class PartnerBase(BaseModel):
    enabled: bool = True
    sort_order: int = 0
    flag: str = ""
    country_uz: str
    country_ru: str
    country_en: str
    count: int = 1
    logo_url: str | None = None
    url: str | None = None


class PartnerCreate(PartnerBase):
    pass


class PartnerUpdate(BaseModel):
    enabled: bool | None = None
    sort_order: int | None = None
    flag: str | None = None
    country_uz: str | None = None
    country_ru: str | None = None
    country_en: str | None = None
    count: int | None = None
    logo_url: str | None = None
    url: str | None = None


class PartnerAdminOut(PartnerBase, ORM):
    id: int


class PartnerPublicOut(BaseModel):
    id: int
    flag: str
    country: str
    count: int
    logo_url: str | None
    url: str | None


# ══════════════════════════════════════════════════════════
#  LICENSE
# ══════════════════════════════════════════════════════════
class LicenseBase(BaseModel):
    enabled: bool = True
    sort_order: int = 0
    title_uz: str
    title_ru: str
    title_en: str
    issuer_uz: str = ""
    issuer_ru: str = ""
    issuer_en: str = ""
    year: int | None = None
    image: str | None = None
    pdf: str | None = None


class LicenseCreate(LicenseBase):
    pass


class LicenseUpdate(BaseModel):
    enabled: bool | None = None
    sort_order: int | None = None
    title_uz: str | None = None
    title_ru: str | None = None
    title_en: str | None = None
    issuer_uz: str | None = None
    issuer_ru: str | None = None
    issuer_en: str | None = None
    year: int | None = None
    image: str | None = None
    pdf: str | None = None


class LicenseAdminOut(LicenseBase, ORM):
    id: int


class LicensePublicOut(BaseModel):
    id: int
    title: str
    issuer: str
    year: int | None
    image: str | None
    pdf: str | None


# ══════════════════════════════════════════════════════════
#  HOME FAQ
# ══════════════════════════════════════════════════════════
class HomeFAQBase(BaseModel):
    enabled: bool = True
    sort_order: int = 0
    question_uz: str
    question_ru: str
    question_en: str
    answer_uz: str
    answer_ru: str
    answer_en: str


class HomeFAQCreate(HomeFAQBase):
    pass


class HomeFAQUpdate(BaseModel):
    enabled: bool | None = None
    sort_order: int | None = None
    question_uz: str | None = None
    question_ru: str | None = None
    question_en: str | None = None
    answer_uz: str | None = None
    answer_ru: str | None = None
    answer_en: str | None = None


class HomeFAQAdminOut(HomeFAQBase, ORM):
    id: int


class HomeFAQPublicOut(BaseModel):
    id: int
    question: str
    answer: str


# ══════════════════════════════════════════════════════════
#  FINAL CTA (singleton)
# ══════════════════════════════════════════════════════════
class FinalCTABase(BaseModel):
    enabled: bool = True
    eyebrow_uz: str | None = None
    eyebrow_ru: str | None = None
    eyebrow_en: str | None = None
    title_uz: str | None = None
    title_ru: str | None = None
    title_en: str | None = None
    text_uz: str | None = None
    text_ru: str | None = None
    text_en: str | None = None
    cta_label_uz: str | None = None
    cta_label_ru: str | None = None
    cta_label_en: str | None = None
    cta_url: str | None = None
    cta_external: bool = False
    phone_label: str | None = None
    phone_url: str | None = None


class FinalCTAUpdate(FinalCTABase):
    pass


class FinalCTAAdminOut(FinalCTABase, ORM):
    id: int
    updated_at: datetime


class FinalCTAPublicOut(BaseModel):
    enabled: bool
    eyebrow: str | None
    title: str | None
    text: str | None
    cta_label: str | None
    cta_url: str | None
    cta_external: bool
    phone_label: str | None
    phone_url: str | None


# ══════════════════════════════════════════════════════════
#  AGGREGATE PUBLIC RESPONSE
# ══════════════════════════════════════════════════════════
class HomePagePublic(BaseModel):
    """Single payload returned by GET /api/page-settings/home."""
    hero: HeroPublicOut | None
    sections: list[SectionPublicOut]
    quick_actions: list[QuickActionPublicOut]
    intro_pillars: list[IntroPillarPublicOut]
    campus: CampusPublicOut | None
    why_cards: list[WhyCardPublicOut]
    faculties: list[FacultyPublicOut]
    admission_steps: list[AdmissionStepPublicOut]
    stats: list[StatPublicOut]
    testimonials: list[TestimonialPublicOut]
    partners: list[PartnerPublicOut]
    licenses: list[LicensePublicOut]
    faqs: list[HomeFAQPublicOut]
    final_cta: FinalCTAPublicOut | None
