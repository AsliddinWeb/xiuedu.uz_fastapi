"""Contact page CMS — singleton."""
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ContactPage(Base):
    __tablename__ = "contact_page"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Hero
    hero_eyebrow_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    hero_eyebrow_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    hero_eyebrow_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    hero_title_uz: Mapped[str | None] = mapped_column(String(500), nullable=True)
    hero_title_ru: Mapped[str | None] = mapped_column(String(500), nullable=True)
    hero_title_en: Mapped[str | None] = mapped_column(String(500), nullable=True)
    hero_subtitle_uz: Mapped[str | None] = mapped_column(Text, nullable=True)
    hero_subtitle_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    hero_subtitle_en: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Info cards
    address_uz: Mapped[str | None] = mapped_column(String(500), nullable=True)
    address_ru: Mapped[str | None] = mapped_column(String(500), nullable=True)
    address_en: Mapped[str | None] = mapped_column(String(500), nullable=True)
    phone:   Mapped[str | None] = mapped_column(String(60), nullable=True)
    email:   Mapped[str | None] = mapped_column(String(255), nullable=True)
    working_hours_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    working_hours_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    working_hours_en: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Form section
    form_title_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    form_title_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    form_title_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    form_subtitle_uz: Mapped[str | None] = mapped_column(Text, nullable=True)
    form_subtitle_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    form_subtitle_en: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Map
    map_embed_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
