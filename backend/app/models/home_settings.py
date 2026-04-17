"""
Home page CMS models.

All settings, content blocks and collections that drive the public
homepage are defined here. Each table is independent so admins can
edit them in isolation; HomeView reads them through one aggregate
endpoint at /api/page-settings/home.
"""
from datetime import datetime

from sqlalchemy import (
    JSON, Boolean, DateTime, ForeignKey, Integer, String, Text, func
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

# JSON variant — JSONB on Postgres, JSON elsewhere (sqlite tests)
JSONField = JSON().with_variant(JSONB(), "postgresql")


# ─────────────────────────────────────────────────────────────────
#  Hero — single row keyed by page slug ("home" only for now)
# ─────────────────────────────────────────────────────────────────
class HeroSettings(Base):
    __tablename__ = "hero_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    page: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)

    # Layout variant: split | fullbleed_photo | video_bg | stats | minimal
    variant: Mapped[str] = mapped_column(String(40), default="split", nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # ── Multilingual text ──
    eyebrow_uz:  Mapped[str | None] = mapped_column(String(255), nullable=True)
    eyebrow_ru:  Mapped[str | None] = mapped_column(String(255), nullable=True)
    eyebrow_en:  Mapped[str | None] = mapped_column(String(255), nullable=True)

    title_uz:    Mapped[str | None] = mapped_column(String(500), nullable=True)
    title_ru:    Mapped[str | None] = mapped_column(String(500), nullable=True)
    title_en:    Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Title can have a highlighted middle word (rendered in accent gold)
    title_highlight_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    title_highlight_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    title_highlight_en: Mapped[str | None] = mapped_column(String(255), nullable=True)

    title_tail_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    title_tail_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    title_tail_en: Mapped[str | None] = mapped_column(String(255), nullable=True)

    subtitle_uz: Mapped[str | None] = mapped_column(Text, nullable=True)
    subtitle_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    subtitle_en: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Media ──
    bg_image:        Mapped[str | None] = mapped_column(String(500), nullable=True)
    bg_video:        Mapped[str | None] = mapped_column(String(500), nullable=True)
    bg_video_poster: Mapped[str | None] = mapped_column(String(500), nullable=True)
    side_image:      Mapped[str | None] = mapped_column(String(500), nullable=True)  # split variant

    overlay_opacity: Mapped[int] = mapped_column(Integer, default=55, nullable=False)  # 0-100

    # ── CTAs ──
    cta_primary_label_uz: Mapped[str | None] = mapped_column(String(120), nullable=True)
    cta_primary_label_ru: Mapped[str | None] = mapped_column(String(120), nullable=True)
    cta_primary_label_en: Mapped[str | None] = mapped_column(String(120), nullable=True)
    cta_primary_url:      Mapped[str | None] = mapped_column(String(500), nullable=True)
    cta_primary_external: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    cta_secondary_label_uz: Mapped[str | None] = mapped_column(String(120), nullable=True)
    cta_secondary_label_ru: Mapped[str | None] = mapped_column(String(120), nullable=True)
    cta_secondary_label_en: Mapped[str | None] = mapped_column(String(120), nullable=True)
    cta_secondary_url:      Mapped[str | None] = mapped_column(String(500), nullable=True)
    cta_secondary_external: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # ── Decorative toggles ──
    show_particles:        Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    show_scroll_indicator: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    show_trust_badges:     Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    show_floating_cards:   Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Optional inline quote (split variant)
    quote_text_uz: Mapped[str | None] = mapped_column(Text, nullable=True)
    quote_text_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    quote_text_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    quote_author_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    quote_author_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    quote_author_en: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Floating badge cards (split variant — TOP-3, 95% etc.)
    badge1_value: Mapped[str | None] = mapped_column(String(40), nullable=True)
    badge1_label_uz: Mapped[str | None] = mapped_column(String(120), nullable=True)
    badge1_label_ru: Mapped[str | None] = mapped_column(String(120), nullable=True)
    badge1_label_en: Mapped[str | None] = mapped_column(String(120), nullable=True)
    badge1_icon:  Mapped[str | None] = mapped_column(String(60), nullable=True)

    badge2_value: Mapped[str | None] = mapped_column(String(40), nullable=True)
    badge2_label_uz: Mapped[str | None] = mapped_column(String(120), nullable=True)
    badge2_label_ru: Mapped[str | None] = mapped_column(String(120), nullable=True)
    badge2_label_en: Mapped[str | None] = mapped_column(String(120), nullable=True)
    badge2_icon:  Mapped[str | None] = mapped_column(String(60), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


# ─────────────────────────────────────────────────────────────────
#  HomeSection — toggle/order/override per section block
# ─────────────────────────────────────────────────────────────────
class HomeSection(Base):
    __tablename__ = "home_sections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String(60), unique=True, index=True, nullable=False)

    enabled:    Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int]  = mapped_column(Integer, default=0, nullable=False)

    # Optional overrides — null means use default i18n key from frontend
    eyebrow_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    eyebrow_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    eyebrow_en: Mapped[str | None] = mapped_column(String(255), nullable=True)

    title_uz: Mapped[str | None] = mapped_column(String(500), nullable=True)
    title_ru: Mapped[str | None] = mapped_column(String(500), nullable=True)
    title_en: Mapped[str | None] = mapped_column(String(500), nullable=True)

    subtitle_uz: Mapped[str | None] = mapped_column(Text, nullable=True)
    subtitle_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    subtitle_en: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Per-section settings (e.g. news limit, columns, bg variant)
    settings: Mapped[dict] = mapped_column(JSONField, default=dict, nullable=False)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


# ─────────────────────────────────────────────────────────────────
#  QuickAction — 4 ribbon cards under hero
# ─────────────────────────────────────────────────────────────────
class QuickAction(Base):
    __tablename__ = "home_quick_actions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enabled:    Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int]  = mapped_column(Integer, default=0, nullable=False)

    icon: Mapped[str] = mapped_column(String(60), nullable=False)  # heroicon name

    title_uz: Mapped[str] = mapped_column(String(200), nullable=False)
    title_ru: Mapped[str] = mapped_column(String(200), nullable=False)
    title_en: Mapped[str] = mapped_column(String(200), nullable=False)

    desc_uz: Mapped[str] = mapped_column(String(300), default="", nullable=False)
    desc_ru: Mapped[str] = mapped_column(String(300), default="", nullable=False)
    desc_en: Mapped[str] = mapped_column(String(300), default="", nullable=False)

    url:      Mapped[str] = mapped_column(String(500), nullable=False)
    external: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    accent:   Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


# ─────────────────────────────────────────────────────────────────
#  IntroPillar — 3 stacked feature cards in intro section
# ─────────────────────────────────────────────────────────────────
class IntroPillar(Base):
    __tablename__ = "home_intro_pillars"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enabled:    Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int]  = mapped_column(Integer, default=0, nullable=False)

    icon: Mapped[str] = mapped_column(String(60), nullable=False)

    title_uz: Mapped[str] = mapped_column(String(200), nullable=False)
    title_ru: Mapped[str] = mapped_column(String(200), nullable=False)
    title_en: Mapped[str] = mapped_column(String(200), nullable=False)

    desc_uz: Mapped[str] = mapped_column(Text, default="", nullable=False)
    desc_ru: Mapped[str] = mapped_column(Text, default="", nullable=False)
    desc_en: Mapped[str] = mapped_column(Text, default="", nullable=False)


# ─────────────────────────────────────────────────────────────────
#  CampusSection — singleton (one row) with images + bullets + video
# ─────────────────────────────────────────────────────────────────
class CampusSection(Base):
    __tablename__ = "home_campus"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    main_image:  Mapped[str | None] = mapped_column(String(500), nullable=True)
    image_2:     Mapped[str | None] = mapped_column(String(500), nullable=True)
    image_3:     Mapped[str | None] = mapped_column(String(500), nullable=True)
    video_url:   Mapped[str | None] = mapped_column(String(500), nullable=True)

    eyebrow_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    eyebrow_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    eyebrow_en: Mapped[str | None] = mapped_column(String(255), nullable=True)

    title_uz: Mapped[str | None] = mapped_column(String(500), nullable=True)
    title_ru: Mapped[str | None] = mapped_column(String(500), nullable=True)
    title_en: Mapped[str | None] = mapped_column(String(500), nullable=True)

    text_uz: Mapped[str | None] = mapped_column(Text, nullable=True)
    text_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    text_en: Mapped[str | None] = mapped_column(Text, nullable=True)

    # bullets stored as list of {uz, ru, en}
    bullets: Mapped[list] = mapped_column(JSONField, default=list, nullable=False)

    cta_label_uz: Mapped[str | None] = mapped_column(String(120), nullable=True)
    cta_label_ru: Mapped[str | None] = mapped_column(String(120), nullable=True)
    cta_label_en: Mapped[str | None] = mapped_column(String(120), nullable=True)
    cta_url:      Mapped[str | None] = mapped_column(String(500), nullable=True)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


# ─────────────────────────────────────────────────────────────────
#  WhyCard — 4 "Why XIU" cards
# ─────────────────────────────────────────────────────────────────
class WhyCard(Base):
    __tablename__ = "home_why_cards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enabled:    Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int]  = mapped_column(Integer, default=0, nullable=False)

    icon:       Mapped[str] = mapped_column(String(60), nullable=False)
    icon_bg:    Mapped[str] = mapped_column(String(60), default="bg-primary-50", nullable=False)
    icon_color: Mapped[str] = mapped_column(String(60), default="text-primary-700", nullable=False)

    number:       Mapped[str] = mapped_column(String(40), default="", nullable=False)
    number_label_uz: Mapped[str] = mapped_column(String(120), default="", nullable=False)
    number_label_ru: Mapped[str] = mapped_column(String(120), default="", nullable=False)
    number_label_en: Mapped[str] = mapped_column(String(120), default="", nullable=False)

    title_uz: Mapped[str] = mapped_column(String(255), nullable=False)
    title_ru: Mapped[str] = mapped_column(String(255), nullable=False)
    title_en: Mapped[str] = mapped_column(String(255), nullable=False)

    desc_uz: Mapped[str] = mapped_column(Text, default="", nullable=False)
    desc_ru: Mapped[str] = mapped_column(Text, default="", nullable=False)
    desc_en: Mapped[str] = mapped_column(Text, default="", nullable=False)


# ─────────────────────────────────────────────────────────────────
#  Faculty + nested programs (used by both Home academic section
#  and the dedicated /faculties pages)
# ─────────────────────────────────────────────────────────────────
class Faculty(Base):
    __tablename__ = "faculties"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)

    enabled:    Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int]  = mapped_column(Integer, default=0, nullable=False)

    icon: Mapped[str] = mapped_column(String(60), nullable=False)

    name_uz: Mapped[str] = mapped_column(String(255), nullable=False)
    name_ru: Mapped[str] = mapped_column(String(255), nullable=False)
    name_en: Mapped[str] = mapped_column(String(255), nullable=False)

    description_uz: Mapped[str] = mapped_column(Text, default="", nullable=False)
    description_ru: Mapped[str] = mapped_column(Text, default="", nullable=False)
    description_en: Mapped[str] = mapped_column(Text, default="", nullable=False)

    cover_image: Mapped[str | None] = mapped_column(String(500), nullable=True)

    programs = relationship(
        "FacultyProgram",
        back_populates="faculty",
        cascade="all, delete-orphan",
        order_by="FacultyProgram.sort_order",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class FacultyProgram(Base):
    __tablename__ = "faculty_programs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    faculty_id: Mapped[int] = mapped_column(
        ForeignKey("faculties.id", ondelete="CASCADE"), nullable=False, index=True
    )

    enabled:    Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int]  = mapped_column(Integer, default=0, nullable=False)

    # Education level — used for filtering and badge colour.
    # Allowed values: "bachelor" | "master" | "short" | "phd"
    level: Mapped[str] = mapped_column(String(20), default="bachelor", server_default="bachelor", nullable=False)

    # Study form — also enum-style for translation on the frontend.
    # Allowed values: "full_time" | "part_time" | "evening" | "online"
    study_form: Mapped[str] = mapped_column(String(20), default="full_time", server_default="full_time", nullable=False)

    name_uz: Mapped[str] = mapped_column(String(300), nullable=False)
    name_ru: Mapped[str] = mapped_column(String(300), nullable=False)
    name_en: Mapped[str] = mapped_column(String(300), nullable=False)

    icon: Mapped[str] = mapped_column(String(60), nullable=False)
    bg_class:      Mapped[str] = mapped_column(String(120), default="bg-indigo-50", nullable=False)
    icon_bg_class: Mapped[str] = mapped_column(String(120), default="bg-indigo-500", nullable=False)
    ring_class:    Mapped[str] = mapped_column(String(120), default="ring-indigo-200/60", nullable=False)

    duration_uz: Mapped[str] = mapped_column(String(60), default="", nullable=False)
    duration_ru: Mapped[str] = mapped_column(String(60), default="", nullable=False)
    duration_en: Mapped[str] = mapped_column(String(60), default="", nullable=False)

    tuition: Mapped[str] = mapped_column(String(60), default="", nullable=False)

    language_uz: Mapped[str] = mapped_column(String(60), default="", nullable=False)
    language_ru: Mapped[str] = mapped_column(String(60), default="", nullable=False)
    language_en: Mapped[str] = mapped_column(String(60), default="", nullable=False)

    # Awarded degree label, multilingual ("Bakalavr diplomi", "MBA", "Sertifikat")
    degree_uz: Mapped[str] = mapped_column(String(120), default="", server_default="", nullable=False)
    degree_ru: Mapped[str] = mapped_column(String(120), default="", server_default="", nullable=False)
    degree_en: Mapped[str] = mapped_column(String(120), default="", server_default="", nullable=False)

    # Numeric extras
    credits: Mapped[int | None] = mapped_column(Integer, nullable=True)
    seats:   Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Multiple study forms with per-form tuition and seats.
    # Each element: { "form": "full_time", "tuition": "16 mln", "seats": 50 }
    # This replaces the single study_form/tuition/seats above (kept for compat).
    study_forms: Mapped[list] = mapped_column(JSONField, default=list, server_default="[]", nullable=False)

    faculty = relationship("Faculty", back_populates="programs")


# ─────────────────────────────────────────────────────────────────
#  AdmissionStep — 4 numbered admission journey steps
# ─────────────────────────────────────────────────────────────────
class AdmissionStep(Base):
    __tablename__ = "home_admission_steps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enabled:    Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int]  = mapped_column(Integer, default=0, nullable=False)

    number: Mapped[str] = mapped_column(String(8), nullable=False)  # "01"
    icon:   Mapped[str] = mapped_column(String(60), nullable=False)

    title_uz: Mapped[str] = mapped_column(String(255), nullable=False)
    title_ru: Mapped[str] = mapped_column(String(255), nullable=False)
    title_en: Mapped[str] = mapped_column(String(255), nullable=False)

    desc_uz: Mapped[str] = mapped_column(Text, default="", nullable=False)
    desc_ru: Mapped[str] = mapped_column(Text, default="", nullable=False)
    desc_en: Mapped[str] = mapped_column(Text, default="", nullable=False)


# ─────────────────────────────────────────────────────────────────
#  Stat — Numbers in Context (4 cards)
# ─────────────────────────────────────────────────────────────────
class Stat(Base):
    __tablename__ = "home_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enabled:    Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int]  = mapped_column(Integer, default=0, nullable=False)

    value: Mapped[str] = mapped_column(String(40), nullable=False)  # "5,000+"

    label_uz: Mapped[str] = mapped_column(String(255), nullable=False)
    label_ru: Mapped[str] = mapped_column(String(255), nullable=False)
    label_en: Mapped[str] = mapped_column(String(255), nullable=False)

    sub_uz: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    sub_ru: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    sub_en: Mapped[str] = mapped_column(String(255), default="", nullable=False)


# ─────────────────────────────────────────────────────────────────
#  Testimonial
# ─────────────────────────────────────────────────────────────────
class Testimonial(Base):
    __tablename__ = "home_testimonials"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enabled:    Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int]  = mapped_column(Integer, default=0, nullable=False)

    name_uz: Mapped[str] = mapped_column(String(255), nullable=False)
    name_ru: Mapped[str] = mapped_column(String(255), nullable=False)
    name_en: Mapped[str] = mapped_column(String(255), nullable=False)

    role_uz: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    role_ru: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    role_en: Mapped[str] = mapped_column(String(255), default="", nullable=False)

    text_uz: Mapped[str] = mapped_column(Text, nullable=False)
    text_ru: Mapped[str] = mapped_column(Text, nullable=False)
    text_en: Mapped[str] = mapped_column(Text, nullable=False)

    avatar: Mapped[str | None] = mapped_column(String(500), nullable=True)
    rating: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    year:   Mapped[int | None] = mapped_column(Integer, nullable=True)


# ─────────────────────────────────────────────────────────────────
#  Partner — international partner countries
# ─────────────────────────────────────────────────────────────────
class Partner(Base):
    __tablename__ = "home_partners"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enabled:    Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int]  = mapped_column(Integer, default=0, nullable=False)

    flag: Mapped[str] = mapped_column(String(20), default="", nullable=False)  # emoji

    country_uz: Mapped[str] = mapped_column(String(120), nullable=False)
    country_ru: Mapped[str] = mapped_column(String(120), nullable=False)
    country_en: Mapped[str] = mapped_column(String(120), nullable=False)

    count:    Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    logo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    url:      Mapped[str | None] = mapped_column(String(500), nullable=True)


# ─────────────────────────────────────────────────────────────────
#  License — A4 accreditation documents
# ─────────────────────────────────────────────────────────────────
class License(Base):
    __tablename__ = "home_licenses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enabled:    Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int]  = mapped_column(Integer, default=0, nullable=False)

    title_uz: Mapped[str] = mapped_column(String(255), nullable=False)
    title_ru: Mapped[str] = mapped_column(String(255), nullable=False)
    title_en: Mapped[str] = mapped_column(String(255), nullable=False)

    issuer_uz: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    issuer_ru: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    issuer_en: Mapped[str] = mapped_column(String(255), default="", nullable=False)

    year:  Mapped[int | None] = mapped_column(Integer, nullable=True)
    image: Mapped[str | None] = mapped_column(String(500), nullable=True)
    pdf:   Mapped[str | None] = mapped_column(String(500), nullable=True)


# ─────────────────────────────────────────────────────────────────
#  HomeFAQ — separate from generic FAQ to keep home content scoped
# ─────────────────────────────────────────────────────────────────
class HomeFAQ(Base):
    __tablename__ = "home_faqs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enabled:    Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int]  = mapped_column(Integer, default=0, nullable=False)

    question_uz: Mapped[str] = mapped_column(String(500), nullable=False)
    question_ru: Mapped[str] = mapped_column(String(500), nullable=False)
    question_en: Mapped[str] = mapped_column(String(500), nullable=False)

    answer_uz: Mapped[str] = mapped_column(Text, nullable=False)
    answer_ru: Mapped[str] = mapped_column(Text, nullable=False)
    answer_en: Mapped[str] = mapped_column(Text, nullable=False)


# ─────────────────────────────────────────────────────────────────
#  FinalCTA — bottom dark CTA strip (singleton)
# ─────────────────────────────────────────────────────────────────
class FinalCTA(Base):
    __tablename__ = "home_final_cta"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    eyebrow_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    eyebrow_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    eyebrow_en: Mapped[str | None] = mapped_column(String(255), nullable=True)

    title_uz: Mapped[str | None] = mapped_column(String(500), nullable=True)
    title_ru: Mapped[str | None] = mapped_column(String(500), nullable=True)
    title_en: Mapped[str | None] = mapped_column(String(500), nullable=True)

    text_uz: Mapped[str | None] = mapped_column(Text, nullable=True)
    text_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    text_en: Mapped[str | None] = mapped_column(Text, nullable=True)

    cta_label_uz: Mapped[str | None] = mapped_column(String(120), nullable=True)
    cta_label_ru: Mapped[str | None] = mapped_column(String(120), nullable=True)
    cta_label_en: Mapped[str | None] = mapped_column(String(120), nullable=True)
    cta_url:      Mapped[str | None] = mapped_column(String(500), nullable=True)
    cta_external: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    phone_label: Mapped[str | None] = mapped_column(String(60), nullable=True)
    phone_url:   Mapped[str | None] = mapped_column(String(60), nullable=True)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
