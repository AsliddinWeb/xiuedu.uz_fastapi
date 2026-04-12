import uuid
from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID

# Use JSONB on Postgres, fall back to JSON elsewhere (sqlite for tests)
GalleryJSON = JSON().with_variant(JSONB(), "postgresql")
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class NewsCategory(Base):
    __tablename__ = "news_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    name_uz: Mapped[str] = mapped_column(String(255), nullable=False)
    name_ru: Mapped[str] = mapped_column(String(255), nullable=False)
    name_en: Mapped[str] = mapped_column(String(255), nullable=False)
    color: Mapped[str | None] = mapped_column(String(20), nullable=True)
    icon: Mapped[str | None] = mapped_column(String(50), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    news = relationship("News", back_populates="category")


class News(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(
        String(300), unique=True, index=True, nullable=False
    )

    title_uz: Mapped[str] = mapped_column(String(500), nullable=False)
    title_ru: Mapped[str] = mapped_column(String(500), nullable=False)
    title_en: Mapped[str] = mapped_column(String(500), nullable=False)

    excerpt_uz: Mapped[str] = mapped_column(String(1000), nullable=False, default="")
    excerpt_ru: Mapped[str] = mapped_column(String(1000), nullable=False, default="")
    excerpt_en: Mapped[str] = mapped_column(String(1000), nullable=False, default="")

    body_uz: Mapped[str] = mapped_column(Text, nullable=False, default="")
    body_ru: Mapped[str] = mapped_column(Text, nullable=False, default="")
    body_en: Mapped[str] = mapped_column(Text, nullable=False, default="")

    cover_image: Mapped[str | None] = mapped_column(String(500), nullable=True)
    gallery: Mapped[list[str]] = mapped_column(GalleryJSON, default=list, nullable=False)

    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    views_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )

    # SEO
    meta_title_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    meta_title_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    meta_title_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    meta_description_uz: Mapped[str | None] = mapped_column(String(500), nullable=True)
    meta_description_ru: Mapped[str | None] = mapped_column(String(500), nullable=True)
    meta_description_en: Mapped[str | None] = mapped_column(String(500), nullable=True)

    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("news_categories.id", ondelete="SET NULL"), nullable=True
    )
    author_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    category = relationship("NewsCategory", back_populates="news")
    author = relationship("User", back_populates="news")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
