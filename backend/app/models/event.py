import uuid
from datetime import datetime

from sqlalchemy import (
    JSON, Boolean, DateTime, ForeignKey, Integer, String, Text, func
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

# JSON variant for sqlite tests + postgres prod
GalleryJSON = JSON().with_variant(JSONB(), "postgresql")


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(300), unique=True, index=True, nullable=False)

    # Multilingual title
    title_uz: Mapped[str] = mapped_column(String(500), nullable=False)
    title_ru: Mapped[str] = mapped_column(String(500), nullable=False)
    title_en: Mapped[str] = mapped_column(String(500), nullable=False)

    # Multilingual description
    description_uz: Mapped[str] = mapped_column(Text, nullable=False, default="")
    description_ru: Mapped[str] = mapped_column(Text, nullable=False, default="")
    description_en: Mapped[str] = mapped_column(Text, nullable=False, default="")

    # When + where
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    location_uz: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    location_ru: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    location_en: Mapped[str] = mapped_column(String(255), nullable=False, default="")

    # Media
    cover_image: Mapped[str | None] = mapped_column(String(500), nullable=True)
    gallery: Mapped[list[str]] = mapped_column(GalleryJSON, default=list, nullable=False)

    # Publishing
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # SEO
    meta_title_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    meta_title_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    meta_title_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    meta_description_uz: Mapped[str | None] = mapped_column(String(500), nullable=True)
    meta_description_ru: Mapped[str | None] = mapped_column(String(500), nullable=True)
    meta_description_en: Mapped[str | None] = mapped_column(String(500), nullable=True)

    author_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
