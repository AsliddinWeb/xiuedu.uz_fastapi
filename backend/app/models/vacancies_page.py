"""
Vacancies page CMS — singleton + Vacancy CRUD.
"""
from datetime import datetime, date

from sqlalchemy import Boolean, Date, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class VacanciesPage(Base):
    __tablename__ = "vacancies_page"

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

    # Empty-state when no vacancies are open
    empty_title_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    empty_title_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    empty_title_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    empty_text_uz: Mapped[str | None] = mapped_column(Text, nullable=True)
    empty_text_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    empty_text_en: Mapped[str | None] = mapped_column(Text, nullable=True)

    # CV submission CTA card (always shown)
    cv_title_uz: Mapped[str | None] = mapped_column(String(255), nullable=True)
    cv_title_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    cv_title_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    cv_text_uz: Mapped[str | None] = mapped_column(Text, nullable=True)
    cv_text_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    cv_text_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    cv_email: Mapped[str | None] = mapped_column(String(255), nullable=True)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class Vacancy(Base):
    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enabled:    Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int]  = mapped_column(Integer, default=0, nullable=False)

    is_open: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    title_uz: Mapped[str] = mapped_column(String(500), nullable=False)
    title_ru: Mapped[str] = mapped_column(String(500), nullable=False)
    title_en: Mapped[str] = mapped_column(String(500), nullable=False)

    department_uz: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    department_ru: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    department_en: Mapped[str] = mapped_column(String(255), default="", nullable=False)

    # Allowed: full_time | part_time | contract | internship | online
    employment_type: Mapped[str] = mapped_column(String(20), default="full_time", server_default="full_time", nullable=False)

    location_uz: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    location_ru: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    location_en: Mapped[str] = mapped_column(String(255), default="", nullable=False)

    description_uz: Mapped[str] = mapped_column(Text, default="", nullable=False)
    description_ru: Mapped[str] = mapped_column(Text, default="", nullable=False)
    description_en: Mapped[str] = mapped_column(Text, default="", nullable=False)

    requirements_uz: Mapped[str] = mapped_column(Text, default="", nullable=False)
    requirements_ru: Mapped[str] = mapped_column(Text, default="", nullable=False)
    requirements_en: Mapped[str] = mapped_column(Text, default="", nullable=False)

    salary: Mapped[str | None] = mapped_column(String(120), nullable=True)
    contact_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    apply_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    posted_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    deadline:  Mapped[date | None] = mapped_column(Date, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
