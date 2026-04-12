"""
International cooperation page CMS — singleton + 2 CRUD collections.
"""
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class InternationalPage(Base):
    __tablename__ = "international_page"

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

    # Stats — 4 small cells (value + label_xx)
    stat1_value: Mapped[str | None] = mapped_column(String(40), nullable=True)
    stat1_label_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    stat1_label_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    stat1_label_en: Mapped[str | None] = mapped_column(String(255), nullable=True)

    stat2_value: Mapped[str | None] = mapped_column(String(40), nullable=True)
    stat2_label_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    stat2_label_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    stat2_label_en: Mapped[str | None] = mapped_column(String(255), nullable=True)

    stat3_value: Mapped[str | None] = mapped_column(String(40), nullable=True)
    stat3_label_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    stat3_label_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    stat3_label_en: Mapped[str | None] = mapped_column(String(255), nullable=True)

    stat4_value: Mapped[str | None] = mapped_column(String(40), nullable=True)
    stat4_label_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    stat4_label_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    stat4_label_en: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Section overrides
    programs_eyebrow_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    programs_eyebrow_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    programs_eyebrow_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    programs_title_uz: Mapped[str | None] = mapped_column(String(500), nullable=True)
    programs_title_ru: Mapped[str | None] = mapped_column(String(500), nullable=True)
    programs_title_en: Mapped[str | None] = mapped_column(String(500), nullable=True)

    partners_eyebrow_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    partners_eyebrow_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    partners_eyebrow_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    partners_title_uz: Mapped[str | None] = mapped_column(String(500), nullable=True)
    partners_title_ru: Mapped[str | None] = mapped_column(String(500), nullable=True)
    partners_title_en: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Contact CTA
    cta_title_uz: Mapped[str | None] = mapped_column(String(500), nullable=True)
    cta_title_ru: Mapped[str | None] = mapped_column(String(500), nullable=True)
    cta_title_en: Mapped[str | None] = mapped_column(String(500), nullable=True)
    cta_text_uz: Mapped[str | None] = mapped_column(Text, nullable=True)
    cta_text_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    cta_text_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    cta_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    cta_phone_label: Mapped[str | None] = mapped_column(String(60), nullable=True)
    cta_phone_url:   Mapped[str | None] = mapped_column(String(60), nullable=True)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class IntlProgram(Base):
    """Exchange / dual diploma / internship / joint research."""
    __tablename__ = "international_programs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enabled:    Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int]  = mapped_column(Integer, default=0, nullable=False)

    icon: Mapped[str] = mapped_column(String(60), nullable=False)

    title_uz: Mapped[str] = mapped_column(String(255), nullable=False)
    title_ru: Mapped[str] = mapped_column(String(255), nullable=False)
    title_en: Mapped[str] = mapped_column(String(255), nullable=False)

    desc_uz: Mapped[str] = mapped_column(Text, default="", nullable=False)
    desc_ru: Mapped[str] = mapped_column(Text, default="", nullable=False)
    desc_en: Mapped[str] = mapped_column(Text, default="", nullable=False)


class IntlPartner(Base):
    """Specific partner universities (different from country chips on home)."""
    __tablename__ = "international_partners"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enabled:    Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int]  = mapped_column(Integer, default=0, nullable=False)

    name: Mapped[str] = mapped_column(String(255), nullable=False)  # University name (rarely translated)
    country_code: Mapped[str] = mapped_column(String(8), default="", nullable=False)  # "GB", "DE"
    flag: Mapped[str] = mapped_column(String(20), default="", nullable=False)  # emoji
    logo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    url:      Mapped[str | None] = mapped_column(String(500), nullable=True)
