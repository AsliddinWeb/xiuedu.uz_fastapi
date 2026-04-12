"""
Leadership / staff model used by the public LeadershipView and the
StructureView. Each row represents a person with their group
(rector / prorector / dean / department_head), multilingual name,
position, degree and bio.
"""
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Leader(Base):
    __tablename__ = "leaders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enabled:    Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int]  = mapped_column(Integer, default=0, nullable=False)

    # Allowed values: "rector" | "prorector" | "dean" | "department_head"
    group: Mapped[str] = mapped_column(String(30), nullable=False, index=True)

    name_uz: Mapped[str] = mapped_column(String(255), nullable=False)
    name_ru: Mapped[str] = mapped_column(String(255), nullable=False)
    name_en: Mapped[str] = mapped_column(String(255), nullable=False)

    position_uz: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    position_ru: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    position_en: Mapped[str] = mapped_column(String(255), default="", nullable=False)

    degree_uz: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    degree_ru: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    degree_en: Mapped[str] = mapped_column(String(255), default="", nullable=False)

    bio_uz: Mapped[str] = mapped_column(Text, default="", nullable=False)
    bio_ru: Mapped[str] = mapped_column(Text, default="", nullable=False)
    bio_en: Mapped[str] = mapped_column(Text, default="", nullable=False)

    photo: Mapped[str | None] = mapped_column(String(500), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(60),  nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
