"""
Global site settings — logo, site name, footer, analytics, etc.
Single row (singleton).
"""
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SiteSettings(Base):
    __tablename__ = "site_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Branding
    site_name_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    site_name_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    site_name_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    site_short_name: Mapped[str | None] = mapped_column(String(60), nullable=True)

    logo_url:      Mapped[str | None] = mapped_column(String(500), nullable=True)
    logo_dark_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    favicon_url:   Mapped[str | None] = mapped_column(String(500), nullable=True)
    og_image_url:  Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Footer
    footer_desc_uz: Mapped[str | None] = mapped_column(Text, nullable=True)
    footer_desc_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    footer_desc_en: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Social links
    telegram_url:  Mapped[str | None] = mapped_column(String(500), nullable=True)
    instagram_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    facebook_url:  Mapped[str | None] = mapped_column(String(500), nullable=True)
    youtube_url:   Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Contact (global — also used in footer)
    phone:   Mapped[str | None] = mapped_column(String(60), nullable=True)
    email:   Mapped[str | None] = mapped_column(String(255), nullable=True)
    address_uz: Mapped[str | None] = mapped_column(String(500), nullable=True)
    address_ru: Mapped[str | None] = mapped_column(String(500), nullable=True)
    address_en: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # External links
    hemis_url:     Mapped[str | None] = mapped_column(String(500), nullable=True)
    admission_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Analytics
    google_analytics_id: Mapped[str | None] = mapped_column(String(60), nullable=True)
    yandex_metrica_id:   Mapped[str | None] = mapped_column(String(60), nullable=True)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
