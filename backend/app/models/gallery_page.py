"""
Gallery page CMS — singleton page + GalleryCategory + GalleryItem.
"""
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class GalleryPage(Base):
    __tablename__ = "gallery_page"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    hero_eyebrow_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    hero_eyebrow_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    hero_eyebrow_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    hero_title_uz: Mapped[str | None] = mapped_column(String(500), nullable=True)
    hero_title_ru: Mapped[str | None] = mapped_column(String(500), nullable=True)
    hero_title_en: Mapped[str | None] = mapped_column(String(500), nullable=True)
    hero_subtitle_uz: Mapped[str | None] = mapped_column(Text, nullable=True)
    hero_subtitle_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    hero_subtitle_en: Mapped[str | None] = mapped_column(Text, nullable=True)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class GalleryCategory(Base):
    __tablename__ = "gallery_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enabled:    Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int]  = mapped_column(Integer, default=0, nullable=False)

    slug: Mapped[str] = mapped_column(String(60), unique=True, index=True, nullable=False)

    name_uz: Mapped[str] = mapped_column(String(120), nullable=False)
    name_ru: Mapped[str] = mapped_column(String(120), nullable=False)
    name_en: Mapped[str] = mapped_column(String(120), nullable=False)

    items = relationship(
        "GalleryItem",
        back_populates="category",
        cascade="all, delete-orphan",
        order_by="GalleryItem.sort_order",
    )


class GalleryItem(Base):
    __tablename__ = "gallery_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("gallery_categories.id", ondelete="CASCADE"), nullable=False, index=True
    )
    enabled:    Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int]  = mapped_column(Integer, default=0, nullable=False)

    image: Mapped[str] = mapped_column(String(500), nullable=False)

    caption_uz: Mapped[str] = mapped_column(String(300), default="", nullable=False)
    caption_ru: Mapped[str] = mapped_column(String(300), default="", nullable=False)
    caption_en: Mapped[str] = mapped_column(String(300), default="", nullable=False)

    alt_uz: Mapped[str] = mapped_column(String(300), default="", nullable=False)
    alt_ru: Mapped[str] = mapped_column(String(300), default="", nullable=False)
    alt_en: Mapped[str] = mapped_column(String(300), default="", nullable=False)

    category = relationship("GalleryCategory", back_populates="items")
