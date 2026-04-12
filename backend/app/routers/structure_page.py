"""
Structure page routes — public aggregate (with rector + faculties
fan-out) + admin CRUD.
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.structure_page import StructurePage, AdminDepartment, SupportService
from app.models.leader import Leader
from app.models.home_settings import Faculty
from app.models.user import Role, User
from app.schemas.structure_page import (
    StructurePageAdminOut, StructurePagePublic, StructurePagePublicAggregate, StructurePageUpdate,
    AdminDepartmentAdminOut, AdminDepartmentCreate, AdminDepartmentPublic, AdminDepartmentUpdate,
    SupportServiceAdminOut, SupportServiceCreate, SupportServicePublic, SupportServiceUpdate,
)
from app.utils.deps import require_roles
from app.utils.lang import Lang, get_lang, pick

# ─────────────────────────────────────────────────────────────────
#  Public
# ─────────────────────────────────────────────────────────────────
public = APIRouter(prefix="/page-settings", tags=["page-settings:structure"])


def _page_public(p: StructurePage | None, lang: Lang):
    if not p:
        return None
    return StructurePagePublic(
        hero_eyebrow=pick(p, "hero_eyebrow", lang),
        hero_title=pick(p, "hero_title", lang),
        hero_subtitle=pick(p, "hero_subtitle", lang),
        top_eyebrow=pick(p, "top_eyebrow", lang),
        top_title=pick(p, "top_title", lang),
        academic_eyebrow=pick(p, "academic_eyebrow", lang),
        academic_title=pick(p, "academic_title", lang),
        academic_lead=pick(p, "academic_lead", lang),
        admin_eyebrow=pick(p, "admin_eyebrow", lang),
        admin_title=pick(p, "admin_title", lang),
        admin_lead=pick(p, "admin_lead", lang),
        services_eyebrow=pick(p, "services_eyebrow", lang),
        services_title=pick(p, "services_title", lang),
        services_lead=pick(p, "services_lead", lang),
        cta_title=pick(p, "cta_title", lang),
        cta_text=pick(p, "cta_text", lang),
        cta_primary_label=pick(p, "cta_primary_label", lang),
        cta_primary_url=p.cta_primary_url,
        cta_secondary_label=pick(p, "cta_secondary_label", lang),
        cta_secondary_url=p.cta_secondary_url,
    )


def _leader_dict(l: Leader, lang: Lang) -> dict:
    return {
        "id": l.id,
        "name": pick(l, "name", lang) or "",
        "position": pick(l, "position", lang) or "",
        "photo": l.photo,
    }


def _faculty_dict(f: Faculty, lang: Lang) -> dict:
    return {
        "id": f.id,
        "slug": f.slug,
        "icon": f.icon,
        "name": pick(f, "name", lang) or "",
        "programs_count": len([p for p in f.programs if p.enabled]),
    }


@public.get("/structure", response_model=StructurePagePublicAggregate)
async def get_structure(
    db: Annotated[AsyncSession, Depends(get_db)],
    lang: Annotated[Lang, Depends(get_lang)],
):
    page = (await db.execute(select(StructurePage).limit(1))).scalar_one_or_none()

    leaders = (await db.execute(
        select(Leader).where(Leader.enabled.is_(True))
                      .order_by(Leader.sort_order, Leader.id)
    )).scalars().all()
    rector = next((l for l in leaders if l.group == "rector"), None)
    prorectors = [l for l in leaders if l.group == "prorector"]

    faculties = (await db.execute(
        select(Faculty).where(Faculty.enabled.is_(True))
                       .options(selectinload(Faculty.programs))
                       .order_by(Faculty.sort_order, Faculty.id)
    )).scalars().all()

    departments = (await db.execute(
        select(AdminDepartment).where(AdminDepartment.enabled.is_(True))
                               .order_by(AdminDepartment.sort_order, AdminDepartment.id)
    )).scalars().all()

    services = (await db.execute(
        select(SupportService).where(SupportService.enabled.is_(True))
                              .order_by(SupportService.sort_order, SupportService.id)
    )).scalars().all()

    return StructurePagePublicAggregate(
        page=_page_public(page, lang),
        rector=_leader_dict(rector, lang) if rector else None,
        prorectors=[_leader_dict(l, lang) for l in prorectors],
        faculties=[_faculty_dict(f, lang) for f in faculties],
        departments=[
            AdminDepartmentPublic(
                id=d.id, icon=d.icon,
                name=pick(d, "name", lang) or "",
                head=pick(d, "head", lang),
                email=d.email, phone=d.phone,
            ) for d in departments
        ],
        services=[
            SupportServicePublic(
                id=s.id, icon=s.icon,
                name=pick(s, "name", lang) or "",
                desc=pick(s, "desc", lang) or "",
            ) for s in services
        ],
    )


# ─────────────────────────────────────────────────────────────────
#  Admin
# ─────────────────────────────────────────────────────────────────
admin = APIRouter(prefix="/admin/structure", tags=["admin:structure"])
_dep = require_roles(Role.ADMIN, Role.CONTENT_MANAGER)


@admin.get("/page", response_model=StructurePageAdminOut)
async def admin_get_page(
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    p = (await db.execute(select(StructurePage).limit(1))).scalar_one_or_none()
    if not p:
        p = StructurePage()
        db.add(p); await db.commit(); await db.refresh(p)
    return p


@admin.put("/page", response_model=StructurePageAdminOut)
async def admin_update_page(
    payload: StructurePageUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    p = (await db.execute(select(StructurePage).limit(1))).scalar_one_or_none()
    if not p:
        p = StructurePage(); db.add(p)
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(p, k, v)
    await db.commit(); await db.refresh(p)
    return p


def _crud(model, base_path: str, out_schema, create_schema, update_schema):
    @admin.get(f"/{base_path}", response_model=list[out_schema], name=f"s_list_{base_path}")
    async def _list(
        db: Annotated[AsyncSession, Depends(get_db)],
        _u: User = Depends(_dep),
    ):
        return (await db.execute(
            select(model).order_by(model.sort_order, model.id)
        )).scalars().all()

    @admin.post(f"/{base_path}", response_model=out_schema, status_code=201, name=f"s_create_{base_path}")
    async def _create(
        payload: create_schema,
        db: Annotated[AsyncSession, Depends(get_db)],
        _u: User = Depends(_dep),
    ):
        obj = model(**payload.model_dump())
        db.add(obj); await db.commit(); await db.refresh(obj)
        return obj

    @admin.put(f"/{base_path}/{{item_id}}", response_model=out_schema, name=f"s_update_{base_path}")
    async def _update(
        item_id: int,
        payload: update_schema,
        db: Annotated[AsyncSession, Depends(get_db)],
        _u: User = Depends(_dep),
    ):
        obj = await db.get(model, item_id)
        if not obj:
            raise HTTPException(404, "Not found")
        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(obj, k, v)
        await db.commit(); await db.refresh(obj)
        return obj

    @admin.delete(f"/{base_path}/{{item_id}}", status_code=204, name=f"s_delete_{base_path}")
    async def _delete(
        item_id: int,
        db: Annotated[AsyncSession, Depends(get_db)],
        _u: User = Depends(_dep),
    ):
        obj = await db.get(model, item_id)
        if not obj:
            raise HTTPException(404, "Not found")
        await db.delete(obj); await db.commit()


_crud(AdminDepartment, "departments", AdminDepartmentAdminOut, AdminDepartmentCreate, AdminDepartmentUpdate)
_crud(SupportService,  "services",    SupportServiceAdminOut,  SupportServiceCreate,  SupportServiceUpdate)
