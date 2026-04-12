"""
About page CMS — three tables:
  * AboutPage      — singleton with hero, rector letter, MVV, address
  * TimelineEvent  — year-anchored events (history)
  * Accreditation  — small badges grid (different from A4 License)
"""
from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

JSONField = JSON().with_variant(JSONB(), "postgresql")


class AboutPage(Base):
    __tablename__ = "about_page"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # ── Hero override (uses default i18n if null) ──
    hero_eyebrow_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    hero_eyebrow_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    hero_eyebrow_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    hero_title_uz: Mapped[str | None] = mapped_column(String(500), nullable=True)
    hero_title_ru: Mapped[str | None] = mapped_column(String(500), nullable=True)
    hero_title_en: Mapped[str | None] = mapped_column(String(500), nullable=True)
    hero_subtitle_uz: Mapped[str | None] = mapped_column(Text, nullable=True)
    hero_subtitle_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    hero_subtitle_en: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Rector welcome ──
    rector_image:    Mapped[str | None] = mapped_column(String(500), nullable=True)
    rector_name_uz:  Mapped[str | None] = mapped_column(String(255), nullable=True)
    rector_name_ru:  Mapped[str | None] = mapped_column(String(255), nullable=True)
    rector_name_en:  Mapped[str | None] = mapped_column(String(255), nullable=True)
    rector_role_uz:  Mapped[str | None] = mapped_column(String(255), nullable=True)
    rector_role_ru:  Mapped[str | None] = mapped_column(String(255), nullable=True)
    rector_role_en:  Mapped[str | None] = mapped_column(String(255), nullable=True)
    rector_degree_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    rector_degree_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    rector_degree_en: Mapped[str | None] = mapped_column(String(255), nullable=True)

    rector_letter_eyebrow_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    rector_letter_eyebrow_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    rector_letter_eyebrow_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    rector_letter_title_uz:   Mapped[str | None] = mapped_column(String(500), nullable=True)
    rector_letter_title_ru:   Mapped[str | None] = mapped_column(String(500), nullable=True)
    rector_letter_title_en:   Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Letter body — paragraphs as a list of {uz, ru, en}
    rector_letter_paragraphs: Mapped[list] = mapped_column(JSONField, default=list, nullable=False)

    # ── Mission / Vision / Values ──
    mvv_eyebrow_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    mvv_eyebrow_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    mvv_eyebrow_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    mvv_title_uz:   Mapped[str | None] = mapped_column(String(500), nullable=True)
    mvv_title_ru:   Mapped[str | None] = mapped_column(String(500), nullable=True)
    mvv_title_en:   Mapped[str | None] = mapped_column(String(500), nullable=True)

    mission_uz: Mapped[str | None] = mapped_column(Text, nullable=True)
    mission_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    mission_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    vision_uz:  Mapped[str | None] = mapped_column(Text, nullable=True)
    vision_ru:  Mapped[str | None] = mapped_column(Text, nullable=True)
    vision_en:  Mapped[str | None] = mapped_column(Text, nullable=True)
    values_uz:  Mapped[str | None] = mapped_column(Text, nullable=True)
    values_ru:  Mapped[str | None] = mapped_column(Text, nullable=True)
    values_en:  Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Map / Address ──
    address_uz: Mapped[str | None] = mapped_column(String(500), nullable=True)
    address_ru: Mapped[str | None] = mapped_column(String(500), nullable=True)
    address_en: Mapped[str | None] = mapped_column(String(500), nullable=True)
    contact_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    map_embed_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class TimelineEvent(Base):
    __tablename__ = "about_timeline_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enabled:    Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int]  = mapped_column(Integer, default=0, nullable=False)

    year: Mapped[str] = mapped_column(String(20), nullable=False)

    title_uz: Mapped[str] = mapped_column(String(300), nullable=False)
    title_ru: Mapped[str] = mapped_column(String(300), nullable=False)
    title_en: Mapped[str] = mapped_column(String(300), nullable=False)

    text_uz: Mapped[str] = mapped_column(Text, default="", nullable=False)
    text_ru: Mapped[str] = mapped_column(Text, default="", nullable=False)
    text_en: Mapped[str] = mapped_column(Text, default="", nullable=False)


class Accreditation(Base):
    __tablename__ = "about_accreditations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enabled:    Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int]  = mapped_column(Integer, default=0, nullable=False)

    code: Mapped[str] = mapped_column(String(60), nullable=False)
    icon: Mapped[str] = mapped_column(String(60), default="ShieldCheckIcon", server_default="ShieldCheckIcon", nullable=False)

    name_uz: Mapped[str] = mapped_column(String(255), nullable=False)
    name_ru: Mapped[str] = mapped_column(String(255), nullable=False)
    name_en: Mapped[str] = mapped_column(String(255), nullable=False)
