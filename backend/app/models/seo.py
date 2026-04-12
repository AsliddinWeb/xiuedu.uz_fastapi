from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class GlobalSEO(Base):
    """Site-wide key/value SEO & general settings."""

    __tablename__ = "global_seo"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    value: Mapped[str] = mapped_column(Text, nullable=False, default="")
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class Redirect(Base):
    __tablename__ = "redirects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    old_path: Mapped[str] = mapped_column(
        String(500), unique=True, index=True, nullable=False
    )
    new_path: Mapped[str] = mapped_column(String(500), nullable=False)
    status_code: Mapped[int] = mapped_column(Integer, default=301, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
