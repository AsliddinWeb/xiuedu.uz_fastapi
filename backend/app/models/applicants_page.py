"""
Applicants page CMS — singleton + 5 CRUD collections.
"""
from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

JSONField = JSON().with_variant(JSONB(), "postgresql")


class ApplicantsPage(Base):
    __tablename__ = "applicants_page"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Hero override
    hero_eyebrow_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    hero_eyebrow_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    hero_eyebrow_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    hero_title_uz: Mapped[str | None] = mapped_column(String(500), nullable=True)
    hero_title_ru: Mapped[str | None] = mapped_column(String(500), nullable=True)
    hero_title_en: Mapped[str | None] = mapped_column(String(500), nullable=True)
    hero_subtitle_uz: Mapped[str | None] = mapped_column(Text, nullable=True)
    hero_subtitle_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    hero_subtitle_en: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Section titles override (eyebrow + title for each block)
    steps_eyebrow_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    steps_eyebrow_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    steps_eyebrow_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    steps_title_uz: Mapped[str | None] = mapped_column(String(500), nullable=True)
    steps_title_ru: Mapped[str | None] = mapped_column(String(500), nullable=True)
    steps_title_en: Mapped[str | None] = mapped_column(String(500), nullable=True)

    forms_eyebrow_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    forms_eyebrow_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    forms_eyebrow_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    forms_title_uz: Mapped[str | None] = mapped_column(String(500), nullable=True)
    forms_title_ru: Mapped[str | None] = mapped_column(String(500), nullable=True)
    forms_title_en: Mapped[str | None] = mapped_column(String(500), nullable=True)

    timeline_eyebrow_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    timeline_eyebrow_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    timeline_eyebrow_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    timeline_title_uz: Mapped[str | None] = mapped_column(String(500), nullable=True)
    timeline_title_ru: Mapped[str | None] = mapped_column(String(500), nullable=True)
    timeline_title_en: Mapped[str | None] = mapped_column(String(500), nullable=True)

    docs_eyebrow_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    docs_eyebrow_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    docs_eyebrow_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    docs_title_uz: Mapped[str | None] = mapped_column(String(500), nullable=True)
    docs_title_ru: Mapped[str | None] = mapped_column(String(500), nullable=True)
    docs_title_en: Mapped[str | None] = mapped_column(String(500), nullable=True)

    faq_eyebrow_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    faq_eyebrow_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    faq_eyebrow_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    faq_title_uz: Mapped[str | None] = mapped_column(String(500), nullable=True)
    faq_title_ru: Mapped[str | None] = mapped_column(String(500), nullable=True)
    faq_title_en: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # CTA strip
    cta_title_uz: Mapped[str | None] = mapped_column(String(500), nullable=True)
    cta_title_ru: Mapped[str | None] = mapped_column(String(500), nullable=True)
    cta_title_en: Mapped[str | None] = mapped_column(String(500), nullable=True)
    cta_text_uz: Mapped[str | None] = mapped_column(Text, nullable=True)
    cta_text_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    cta_text_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    cta_primary_label_uz: Mapped[str | None] = mapped_column(String(120), nullable=True)
    cta_primary_label_ru: Mapped[str | None] = mapped_column(String(120), nullable=True)
    cta_primary_label_en: Mapped[str | None] = mapped_column(String(120), nullable=True)
    cta_primary_url:      Mapped[str | None] = mapped_column(String(500), nullable=True)
    cta_primary_external: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    cta_phone_label: Mapped[str | None] = mapped_column(String(60), nullable=True)
    cta_phone_url:   Mapped[str | None] = mapped_column(String(60), nullable=True)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class ApplicantsStep(Base):
    __tablename__ = "applicants_steps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enabled:    Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int]  = mapped_column(Integer, default=0, nullable=False)

    number: Mapped[int] = mapped_column(Integer, nullable=False)
    icon:   Mapped[str] = mapped_column(String(60), nullable=False)

    title_uz: Mapped[str] = mapped_column(String(255), nullable=False)
    title_ru: Mapped[str] = mapped_column(String(255), nullable=False)
    title_en: Mapped[str] = mapped_column(String(255), nullable=False)

    desc_uz: Mapped[str] = mapped_column(Text, default="", nullable=False)
    desc_ru: Mapped[str] = mapped_column(Text, default="", nullable=False)
    desc_en: Mapped[str] = mapped_column(Text, default="", nullable=False)


class ApplicantsForm(Base):
    """Study forms — Kunduzgi / Sirtqi card."""
    __tablename__ = "applicants_forms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enabled:    Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int]  = mapped_column(Integer, default=0, nullable=False)

    title_uz: Mapped[str] = mapped_column(String(300), nullable=False)
    title_ru: Mapped[str] = mapped_column(String(300), nullable=False)
    title_en: Mapped[str] = mapped_column(String(300), nullable=False)

    desc_uz: Mapped[str] = mapped_column(Text, default="", nullable=False)
    desc_ru: Mapped[str] = mapped_column(Text, default="", nullable=False)
    desc_en: Mapped[str] = mapped_column(Text, default="", nullable=False)

    # features stored as list of {uz, ru, en}
    features: Mapped[list] = mapped_column(JSONField, default=list, nullable=False)

    cta_label_uz: Mapped[str | None] = mapped_column(String(120), nullable=True)
    cta_label_ru: Mapped[str | None] = mapped_column(String(120), nullable=True)
    cta_label_en: Mapped[str | None] = mapped_column(String(120), nullable=True)
    cta_url: Mapped[str | None] = mapped_column(String(500), nullable=True)


class ApplicantsTimelineItem(Base):
    __tablename__ = "applicants_timeline"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enabled:    Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int]  = mapped_column(Integer, default=0, nullable=False)

    month_uz: Mapped[str] = mapped_column(String(60), nullable=False)
    month_ru: Mapped[str] = mapped_column(String(60), nullable=False)
    month_en: Mapped[str] = mapped_column(String(60), nullable=False)

    text_uz: Mapped[str] = mapped_column(Text, default="", nullable=False)
    text_ru: Mapped[str] = mapped_column(Text, default="", nullable=False)
    text_en: Mapped[str] = mapped_column(Text, default="", nullable=False)


class ApplicantsDocCategory(Base):
    __tablename__ = "applicants_doc_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enabled:    Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int]  = mapped_column(Integer, default=0, nullable=False)

    title_uz: Mapped[str] = mapped_column(String(300), nullable=False)
    title_ru: Mapped[str] = mapped_column(String(300), nullable=False)
    title_en: Mapped[str] = mapped_column(String(300), nullable=False)

    # items stored as list of {uz, ru, en}
    items: Mapped[list] = mapped_column(JSONField, default=list, nullable=False)


class ApplicantsFaq(Base):
    __tablename__ = "applicants_faqs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enabled:    Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int]  = mapped_column(Integer, default=0, nullable=False)

    question_uz: Mapped[str] = mapped_column(String(500), nullable=False)
    question_ru: Mapped[str] = mapped_column(String(500), nullable=False)
    question_en: Mapped[str] = mapped_column(String(500), nullable=False)

    answer_uz: Mapped[str] = mapped_column(Text, nullable=False)
    answer_ru: Mapped[str] = mapped_column(Text, nullable=False)
    answer_en: Mapped[str] = mapped_column(Text, nullable=False)
