"""
Structure page CMS — singleton + 2 CRUD collections.
Reuses Leader and Faculty models for top management and academic units.
"""
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class StructurePage(Base):
    __tablename__ = "structure_page"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Hero override (uses default i18n if null)
    hero_eyebrow_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    hero_eyebrow_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    hero_eyebrow_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    hero_title_uz: Mapped[str | None] = mapped_column(String(500), nullable=True)
    hero_title_ru: Mapped[str | None] = mapped_column(String(500), nullable=True)
    hero_title_en: Mapped[str | None] = mapped_column(String(500), nullable=True)
    hero_subtitle_uz: Mapped[str | None] = mapped_column(Text, nullable=True)
    hero_subtitle_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    hero_subtitle_en: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Section overrides
    top_eyebrow_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    top_eyebrow_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    top_eyebrow_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    top_title_uz: Mapped[str | None] = mapped_column(String(500), nullable=True)
    top_title_ru: Mapped[str | None] = mapped_column(String(500), nullable=True)
    top_title_en: Mapped[str | None] = mapped_column(String(500), nullable=True)

    academic_eyebrow_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    academic_eyebrow_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    academic_eyebrow_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    academic_title_uz: Mapped[str | None] = mapped_column(String(500), nullable=True)
    academic_title_ru: Mapped[str | None] = mapped_column(String(500), nullable=True)
    academic_title_en: Mapped[str | None] = mapped_column(String(500), nullable=True)
    academic_lead_uz: Mapped[str | None] = mapped_column(Text, nullable=True)
    academic_lead_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    academic_lead_en: Mapped[str | None] = mapped_column(Text, nullable=True)

    admin_eyebrow_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    admin_eyebrow_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    admin_eyebrow_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    admin_title_uz: Mapped[str | None] = mapped_column(String(500), nullable=True)
    admin_title_ru: Mapped[str | None] = mapped_column(String(500), nullable=True)
    admin_title_en: Mapped[str | None] = mapped_column(String(500), nullable=True)
    admin_lead_uz: Mapped[str | None] = mapped_column(Text, nullable=True)
    admin_lead_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    admin_lead_en: Mapped[str | None] = mapped_column(Text, nullable=True)

    services_eyebrow_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    services_eyebrow_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    services_eyebrow_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    services_title_uz: Mapped[str | None] = mapped_column(String(500), nullable=True)
    services_title_ru: Mapped[str | None] = mapped_column(String(500), nullable=True)
    services_title_en: Mapped[str | None] = mapped_column(String(500), nullable=True)
    services_lead_uz: Mapped[str | None] = mapped_column(Text, nullable=True)
    services_lead_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    services_lead_en: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Bottom CTA
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
    cta_secondary_label_uz: Mapped[str | None] = mapped_column(String(120), nullable=True)
    cta_secondary_label_ru: Mapped[str | None] = mapped_column(String(120), nullable=True)
    cta_secondary_label_en: Mapped[str | None] = mapped_column(String(120), nullable=True)
    cta_secondary_url:      Mapped[str | None] = mapped_column(String(500), nullable=True)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class AdminDepartment(Base):
    """Administrative departments grid (10 tile cards)."""
    __tablename__ = "structure_admin_departments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enabled:    Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int]  = mapped_column(Integer, default=0, nullable=False)

    icon: Mapped[str] = mapped_column(String(60), nullable=False)

    name_uz: Mapped[str] = mapped_column(String(255), nullable=False)
    name_ru: Mapped[str] = mapped_column(String(255), nullable=False)
    name_en: Mapped[str] = mapped_column(String(255), nullable=False)

    head_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    head_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    head_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email:   Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone:   Mapped[str | None] = mapped_column(String(60),  nullable=True)


class SupportService(Base):
    """Library, language centre, career, etc."""
    __tablename__ = "structure_support_services"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enabled:    Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int]  = mapped_column(Integer, default=0, nullable=False)

    icon: Mapped[str] = mapped_column(String(60), nullable=False)

    name_uz: Mapped[str] = mapped_column(String(255), nullable=False)
    name_ru: Mapped[str] = mapped_column(String(255), nullable=False)
    name_en: Mapped[str] = mapped_column(String(255), nullable=False)

    desc_uz: Mapped[str] = mapped_column(Text, default="", nullable=False)
    desc_ru: Mapped[str] = mapped_column(Text, default="", nullable=False)
    desc_en: Mapped[str] = mapped_column(Text, default="", nullable=False)
