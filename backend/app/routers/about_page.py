"""
About page routes — public aggregate + admin CRUD.
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.about_page import AboutPage, TimelineEvent, Accreditation
from app.models.user import Role, User
from app.schemas.about_page import (
    AboutPageAdminOut, AboutPagePublic, AboutPagePublicAggregate, AboutPageUpdate,
    AccreditationAdminOut, AccreditationCreate, AccreditationPublicOut, AccreditationUpdate,
    TimelineEventAdminOut, TimelineEventCreate, TimelineEventPublicOut, TimelineEventUpdate,
)
from app.utils.deps import require_roles
from app.utils.lang import Lang, get_lang, pick

# ─────────────────────────────────────────────────────────────────
#  Public
# ─────────────────────────────────────────────────────────────────
public = APIRouter(prefix="/page-settings", tags=["page-settings:about"])


def _about_public(p: AboutPage | None, lang: Lang) -> AboutPagePublic | None:
    if not p:
        return None
    paragraphs = []
    for para in (p.rector_letter_paragraphs or []):
        if isinstance(para, dict):
            text = para.get(lang) or para.get("uz") or ""
            if text:
                paragraphs.append(text)
    return AboutPagePublic(
        hero_eyebrow=pick(p, "hero_eyebrow", lang),
        hero_title=pick(p, "hero_title", lang),
        hero_subtitle=pick(p, "hero_subtitle", lang),

        rector_image=p.rector_image,
        rector_name=pick(p, "rector_name", lang),
        rector_role=pick(p, "rector_role", lang),
        rector_degree=pick(p, "rector_degree", lang),

        rector_letter_eyebrow=pick(p, "rector_letter_eyebrow", lang),
        rector_letter_title=pick(p, "rector_letter_title", lang),
        rector_letter_paragraphs=paragraphs,

        mvv_eyebrow=pick(p, "mvv_eyebrow", lang),
        mvv_title=pick(p, "mvv_title", lang),
        mission=pick(p, "mission", lang),
        vision=pick(p, "vision", lang),
        values=pick(p, "values", lang),

        address=pick(p, "address", lang),
        contact_email=p.contact_email,
        map_embed_url=p.map_embed_url,
    )


@public.get("/about", response_model=AboutPagePublicAggregate)
async def get_about_settings(
    db: Annotated[AsyncSession, Depends(get_db)],
    lang: Annotated[Lang, Depends(get_lang)],
):
    page = (await db.execute(select(AboutPage).limit(1))).scalar_one_or_none()
    timeline = (await db.execute(
        select(TimelineEvent).where(TimelineEvent.enabled.is_(True))
                             .order_by(TimelineEvent.sort_order, TimelineEvent.id)
    )).scalars().all()
    accreditations = (await db.execute(
        select(Accreditation).where(Accreditation.enabled.is_(True))
                             .order_by(Accreditation.sort_order, Accreditation.id)
    )).scalars().all()
    return AboutPagePublicAggregate(
        page=_about_public(page, lang),
        timeline=[
            TimelineEventPublicOut(
                id=t.id, year=t.year,
                title=pick(t, "title", lang) or "",
                text=pick(t, "text", lang) or "",
            ) for t in timeline
        ],
        accreditations=[
            AccreditationPublicOut(
                id=a.id, code=a.code, icon=a.icon,
                name=pick(a, "name", lang) or "",
            ) for a in accreditations
        ],
    )


# ─────────────────────────────────────────────────────────────────
#  Admin
# ─────────────────────────────────────────────────────────────────
admin = APIRouter(prefix="/admin/about", tags=["admin:about"])
_dep = require_roles(Role.ADMIN, Role.CONTENT_MANAGER)


# ── Page singleton ──
@admin.get("/page", response_model=AboutPageAdminOut)
async def admin_get_page(
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    p = (await db.execute(select(AboutPage).limit(1))).scalar_one_or_none()
    if not p:
        p = AboutPage(rector_letter_paragraphs=[])
        db.add(p)
        await db.commit()
        await db.refresh(p)
    return p


@admin.put("/page", response_model=AboutPageAdminOut)
async def admin_update_page(
    payload: AboutPageUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    p = (await db.execute(select(AboutPage).limit(1))).scalar_one_or_none()
    if not p:
        p = AboutPage(rector_letter_paragraphs=[])
        db.add(p)
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(p, k, v)
    await db.commit()
    await db.refresh(p)
    return p


# ── Timeline CRUD ──
@admin.get("/timeline", response_model=list[TimelineEventAdminOut])
async def admin_list_timeline(
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    return (await db.execute(
        select(TimelineEvent).order_by(TimelineEvent.sort_order, TimelineEvent.id)
    )).scalars().all()


@admin.post("/timeline", response_model=TimelineEventAdminOut, status_code=201)
async def admin_create_timeline(
    payload: TimelineEventCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    obj = TimelineEvent(**payload.model_dump())
    db.add(obj); await db.commit(); await db.refresh(obj)
    return obj


@admin.put("/timeline/{item_id}", response_model=TimelineEventAdminOut)
async def admin_update_timeline(
    item_id: int,
    payload: TimelineEventUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    obj = await db.get(TimelineEvent, item_id)
    if not obj:
        raise HTTPException(404, "Not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.commit(); await db.refresh(obj)
    return obj


@admin.delete("/timeline/{item_id}", status_code=204)
async def admin_delete_timeline(
    item_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    obj = await db.get(TimelineEvent, item_id)
    if not obj:
        raise HTTPException(404, "Not found")
    await db.delete(obj); await db.commit()


# ── Accreditation CRUD ──
@admin.get("/accreditations", response_model=list[AccreditationAdminOut])
async def admin_list_accreditations(
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    return (await db.execute(
        select(Accreditation).order_by(Accreditation.sort_order, Accreditation.id)
    )).scalars().all()


@admin.post("/accreditations", response_model=AccreditationAdminOut, status_code=201)
async def admin_create_accreditation(
    payload: AccreditationCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    obj = Accreditation(**payload.model_dump())
    db.add(obj); await db.commit(); await db.refresh(obj)
    return obj


@admin.put("/accreditations/{item_id}", response_model=AccreditationAdminOut)
async def admin_update_accreditation(
    item_id: int,
    payload: AccreditationUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    obj = await db.get(Accreditation, item_id)
    if not obj:
        raise HTTPException(404, "Not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.commit(); await db.refresh(obj)
    return obj


@admin.delete("/accreditations/{item_id}", status_code=204)
async def admin_delete_accreditation(
    item_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    obj = await db.get(Accreditation, item_id)
    if not obj:
        raise HTTPException(404, "Not found")
    await db.delete(obj); await db.commit()
