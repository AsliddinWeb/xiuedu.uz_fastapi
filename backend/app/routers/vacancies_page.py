"""
Vacancies page routes — public aggregate + admin CRUD.
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.vacancies_page import VacanciesPage, Vacancy
from app.models.user import Role, User
from app.schemas.vacancies_page import (
    VacanciesPageAdminOut, VacanciesPagePublic, VacanciesPagePublicAggregate, VacanciesPageUpdate,
    VacancyAdminOut, VacancyCreate, VacancyPublic, VacancyUpdate,
)
from app.utils.deps import require_roles
from app.utils.lang import Lang, get_lang, pick

# ─────────────────────────────────────────────────────────────────
#  Public
# ─────────────────────────────────────────────────────────────────
public = APIRouter(prefix="/page-settings", tags=["page-settings:vacancies"])


def _page_public(p: VacanciesPage | None, lang: Lang):
    if not p:
        return None
    return VacanciesPagePublic(
        hero_eyebrow=pick(p, "hero_eyebrow", lang),
        hero_title=pick(p, "hero_title", lang),
        hero_subtitle=pick(p, "hero_subtitle", lang),
        empty_title=pick(p, "empty_title", lang),
        empty_text=pick(p, "empty_text", lang),
        cv_title=pick(p, "cv_title", lang),
        cv_text=pick(p, "cv_text", lang),
        cv_email=p.cv_email,
    )


def _vacancy_public(v: Vacancy, lang: Lang) -> VacancyPublic:
    return VacancyPublic(
        id=v.id,
        is_open=v.is_open,
        title=pick(v, "title", lang) or "",
        department=pick(v, "department", lang) or "",
        employment_type=v.employment_type,
        location=pick(v, "location", lang) or "",
        description=pick(v, "description", lang) or "",
        requirements=pick(v, "requirements", lang) or "",
        salary=v.salary,
        contact_email=v.contact_email,
        apply_url=v.apply_url,
        posted_at=v.posted_at,
        deadline=v.deadline,
    )


@public.get("/vacancies", response_model=VacanciesPagePublicAggregate)
async def get_vacancies(
    db: Annotated[AsyncSession, Depends(get_db)],
    lang: Annotated[Lang, Depends(get_lang)],
):
    page = (await db.execute(select(VacanciesPage).limit(1))).scalar_one_or_none()
    rows = (await db.execute(
        select(Vacancy).where(Vacancy.enabled.is_(True))
                       .order_by(Vacancy.sort_order, Vacancy.id.desc())
    )).scalars().all()

    vacancies = [_vacancy_public(v, lang) for v in rows]
    departments = sorted({v.department for v in vacancies if v.department})

    return VacanciesPagePublicAggregate(
        page=_page_public(page, lang),
        vacancies=vacancies,
        departments=departments,
    )


# ─────────────────────────────────────────────────────────────────
#  Admin
# ─────────────────────────────────────────────────────────────────
admin = APIRouter(prefix="/admin/vacancies", tags=["admin:vacancies"])
_dep = require_roles(Role.ADMIN, Role.CONTENT_MANAGER)


# Singleton
@admin.get("/page", response_model=VacanciesPageAdminOut)
async def admin_get_page(
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    p = (await db.execute(select(VacanciesPage).limit(1))).scalar_one_or_none()
    if not p:
        p = VacanciesPage()
        db.add(p); await db.commit(); await db.refresh(p)
    return p


@admin.put("/page", response_model=VacanciesPageAdminOut)
async def admin_update_page(
    payload: VacanciesPageUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    p = (await db.execute(select(VacanciesPage).limit(1))).scalar_one_or_none()
    if not p:
        p = VacanciesPage(); db.add(p)
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(p, k, v)
    await db.commit(); await db.refresh(p)
    return p


# Vacancies CRUD
@admin.get("/", response_model=list[VacancyAdminOut])
async def admin_list_vacancies(
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    return (await db.execute(
        select(Vacancy).order_by(Vacancy.sort_order, Vacancy.id.desc())
    )).scalars().all()


@admin.post("/", response_model=VacancyAdminOut, status_code=201)
async def admin_create_vacancy(
    payload: VacancyCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    obj = Vacancy(**payload.model_dump())
    db.add(obj); await db.commit(); await db.refresh(obj)
    return obj


@admin.put("/{item_id}", response_model=VacancyAdminOut)
async def admin_update_vacancy(
    item_id: int,
    payload: VacancyUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    obj = await db.get(Vacancy, item_id)
    if not obj:
        raise HTTPException(404, "Not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.commit(); await db.refresh(obj)
    return obj


@admin.delete("/{item_id}", status_code=204)
async def admin_delete_vacancy(
    item_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    obj = await db.get(Vacancy, item_id)
    if not obj:
        raise HTTPException(404, "Not found")
    await db.delete(obj); await db.commit()
