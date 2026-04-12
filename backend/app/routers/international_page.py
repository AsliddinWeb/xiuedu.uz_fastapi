"""
International page routes — public aggregate + admin CRUD.
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.international_page import InternationalPage, IntlProgram, IntlPartner
from app.models.user import Role, User
from app.schemas.international_page import (
    IntlPageAdminOut, IntlPagePublic, IntlPagePublicAggregate, IntlPageUpdate, IntlStat,
    IntlProgramAdminOut, IntlProgramCreate, IntlProgramPublic, IntlProgramUpdate,
    IntlPartnerAdminOut, IntlPartnerCreate, IntlPartnerPublic, IntlPartnerUpdate,
)
from app.utils.deps import require_roles
from app.utils.lang import Lang, get_lang, pick

# ─────────────────────────────────────────────────────────────────
#  Public
# ─────────────────────────────────────────────────────────────────
public = APIRouter(prefix="/page-settings", tags=["page-settings:international"])


def _stat(value, label_uz, label_ru, label_en, lang) -> IntlStat:
    label = {"uz": label_uz, "ru": label_ru, "en": label_en}.get(lang) or label_uz
    return IntlStat(value=value, label=label)


def _page_public(p: InternationalPage | None, lang: Lang):
    if not p:
        return None
    return IntlPagePublic(
        hero_eyebrow=pick(p, "hero_eyebrow", lang),
        hero_title=pick(p, "hero_title", lang),
        hero_subtitle=pick(p, "hero_subtitle", lang),
        stats=[
            _stat(p.stat1_value, p.stat1_label_uz, p.stat1_label_ru, p.stat1_label_en, lang),
            _stat(p.stat2_value, p.stat2_label_uz, p.stat2_label_ru, p.stat2_label_en, lang),
            _stat(p.stat3_value, p.stat3_label_uz, p.stat3_label_ru, p.stat3_label_en, lang),
            _stat(p.stat4_value, p.stat4_label_uz, p.stat4_label_ru, p.stat4_label_en, lang),
        ],
        programs_eyebrow=pick(p, "programs_eyebrow", lang),
        programs_title=pick(p, "programs_title", lang),
        partners_eyebrow=pick(p, "partners_eyebrow", lang),
        partners_title=pick(p, "partners_title", lang),
        cta_title=pick(p, "cta_title", lang),
        cta_text=pick(p, "cta_text", lang),
        cta_email=p.cta_email,
        cta_phone_label=p.cta_phone_label,
        cta_phone_url=p.cta_phone_url,
    )


@public.get("/international", response_model=IntlPagePublicAggregate)
async def get_international(
    db: Annotated[AsyncSession, Depends(get_db)],
    lang: Annotated[Lang, Depends(get_lang)],
):
    page = (await db.execute(select(InternationalPage).limit(1))).scalar_one_or_none()
    programs = (await db.execute(
        select(IntlProgram).where(IntlProgram.enabled.is_(True))
                           .order_by(IntlProgram.sort_order, IntlProgram.id)
    )).scalars().all()
    partners = (await db.execute(
        select(IntlPartner).where(IntlPartner.enabled.is_(True))
                           .order_by(IntlPartner.sort_order, IntlPartner.id)
    )).scalars().all()

    return IntlPagePublicAggregate(
        page=_page_public(page, lang),
        programs=[IntlProgramPublic(
            id=p.id, icon=p.icon,
            title=pick(p, "title", lang) or "",
            desc=pick(p, "desc", lang) or "",
        ) for p in programs],
        partners=[IntlPartnerPublic(
            id=p.id, name=p.name, country_code=p.country_code,
            flag=p.flag, logo_url=p.logo_url, url=p.url,
        ) for p in partners],
    )


# ─────────────────────────────────────────────────────────────────
#  Admin
# ─────────────────────────────────────────────────────────────────
admin = APIRouter(prefix="/admin/international", tags=["admin:international"])
_dep = require_roles(Role.ADMIN, Role.CONTENT_MANAGER)


@admin.get("/page", response_model=IntlPageAdminOut)
async def admin_get_page(
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    p = (await db.execute(select(InternationalPage).limit(1))).scalar_one_or_none()
    if not p:
        p = InternationalPage()
        db.add(p); await db.commit(); await db.refresh(p)
    return p


@admin.put("/page", response_model=IntlPageAdminOut)
async def admin_update_page(
    payload: IntlPageUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    p = (await db.execute(select(InternationalPage).limit(1))).scalar_one_or_none()
    if not p:
        p = InternationalPage(); db.add(p)
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(p, k, v)
    await db.commit(); await db.refresh(p)
    return p


def _crud(model, base_path: str, out_schema, create_schema, update_schema):
    @admin.get(f"/{base_path}", response_model=list[out_schema], name=f"i_list_{base_path}")
    async def _list(
        db: Annotated[AsyncSession, Depends(get_db)],
        _u: User = Depends(_dep),
    ):
        return (await db.execute(
            select(model).order_by(model.sort_order, model.id)
        )).scalars().all()

    @admin.post(f"/{base_path}", response_model=out_schema, status_code=201, name=f"i_create_{base_path}")
    async def _create(
        payload: create_schema,
        db: Annotated[AsyncSession, Depends(get_db)],
        _u: User = Depends(_dep),
    ):
        obj = model(**payload.model_dump())
        db.add(obj); await db.commit(); await db.refresh(obj)
        return obj

    @admin.put(f"/{base_path}/{{item_id}}", response_model=out_schema, name=f"i_update_{base_path}")
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

    @admin.delete(f"/{base_path}/{{item_id}}", status_code=204, name=f"i_delete_{base_path}")
    async def _delete(
        item_id: int,
        db: Annotated[AsyncSession, Depends(get_db)],
        _u: User = Depends(_dep),
    ):
        obj = await db.get(model, item_id)
        if not obj:
            raise HTTPException(404, "Not found")
        await db.delete(obj); await db.commit()


_crud(IntlProgram, "programs", IntlProgramAdminOut, IntlProgramCreate, IntlProgramUpdate)
_crud(IntlPartner, "partners", IntlPartnerAdminOut, IntlPartnerCreate, IntlPartnerUpdate)
