import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class StaticPage(Base):
    """CMS-managed static page with hierarchy & multilingual SEO."""

    __tablename__ = "static_pages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    is_published: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    page_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Multilingual title
    title_uz: Mapped[str] = mapped_column(String(500), nullable=False)
    title_ru: Mapped[str] = mapped_column(String(500), nullable=False)
    title_en: Mapped[str] = mapped_column(String(500), nullable=False)

    # Multilingual rich content (HTML or JSON)
    content_uz: Mapped[str] = mapped_column(Text, nullable=False, default="")
    content_ru: Mapped[str] = mapped_column(Text, nullable=False, default="")
    content_en: Mapped[str] = mapped_column(Text, nullable=False, default="")

    # SEO
    meta_title_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    meta_title_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    meta_title_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    meta_description_uz: Mapped[str | None] = mapped_column(String(500), nullable=True)
    meta_description_ru: Mapped[str | None] = mapped_column(String(500), nullable=True)
    meta_description_en: Mapped[str | None] = mapped_column(String(500), nullable=True)
    og_image: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Hierarchy (self-referential)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("static_pages.id", ondelete="SET NULL"), nullable=True, index=True
    )
    parent = relationship("StaticPage", remote_side="StaticPage.id", backref="children")

    # Audit
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    creator = relationship("User", back_populates="pages")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
