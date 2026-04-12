"""
Applicants page routes — public aggregate + admin CRUD.
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.applicants_page import (
    ApplicantsPage, ApplicantsStep, ApplicantsForm,
    ApplicantsTimelineItem, ApplicantsDocCategory, ApplicantsFaq,
)
from app.models.user import Role, User
from app.schemas.applicants_page import (
    ApplicantsPageAdminOut, ApplicantsPagePublic, ApplicantsPagePublicAggregate, ApplicantsPageUpdate,
    StepAdminOut, StepCreate, StepPublic, StepUpdate,
    FormAdminOut, FormCreate, FormPublic, FormUpdate,
    TimelineAdminOut, TimelineCreate, TimelinePublic, TimelineUpdate,
    DocAdminOut, DocCreate, DocPublic, DocUpdate,
    FaqAdminOut, FaqCreate, FaqPublic, FaqUpdate,
)
from app.utils.deps import require_roles
from app.utils.lang import Lang, get_lang, pick

# ─────────────────────────────────────────────────────────────────
#  Public
# ─────────────────────────────────────────────────────────────────
public = APIRouter(prefix="/page-settings", tags=["page-settings:applicants"])


def _localize_list(items, lang):
    out = []
    for it in (items or []):
        if isinstance(it, dict):
            v = it.get(lang) or it.get("uz") or ""
            if v:
                out.append(v)
    return out


def _page_public(p: ApplicantsPage | None, lang: Lang):
    if not p:
        return None
    return ApplicantsPagePublic(
        hero_eyebrow=pick(p, "hero_eyebrow", lang),
        hero_title=pick(p, "hero_title", lang),
        hero_subtitle=pick(p, "hero_subtitle", lang),
        steps_eyebrow=pick(p, "steps_eyebrow", lang),
        steps_title=pick(p, "steps_title", lang),
        forms_eyebrow=pick(p, "forms_eyebrow", lang),
        forms_title=pick(p, "forms_title", lang),
        timeline_eyebrow=pick(p, "timeline_eyebrow", lang),
        timeline_title=pick(p, "timeline_title", lang),
        docs_eyebrow=pick(p, "docs_eyebrow", lang),
        docs_title=pick(p, "docs_title", lang),
        faq_eyebrow=pick(p, "faq_eyebrow", lang),
        faq_title=pick(p, "faq_title", lang),
        cta_title=pick(p, "cta_title", lang),
        cta_text=pick(p, "cta_text", lang),
        cta_primary_label=pick(p, "cta_primary_label", lang),
        cta_primary_url=p.cta_primary_url,
        cta_primary_external=p.cta_primary_external,
        cta_phone_label=p.cta_phone_label,
        cta_phone_url=p.cta_phone_url,
    )


@public.get("/applicants", response_model=ApplicantsPagePublicAggregate)
async def get_applicants(
    db: Annotated[AsyncSession, Depends(get_db)],
    lang: Annotated[Lang, Depends(get_lang)],
):
    page = (await db.execute(select(ApplicantsPage).limit(1))).scalar_one_or_none()
    steps = (await db.execute(
        select(ApplicantsStep).where(ApplicantsStep.enabled.is_(True))
                              .order_by(ApplicantsStep.sort_order, ApplicantsStep.id)
    )).scalars().all()
    forms = (await db.execute(
        select(ApplicantsForm).where(ApplicantsForm.enabled.is_(True))
                              .order_by(ApplicantsForm.sort_order, ApplicantsForm.id)
    )).scalars().all()
    timeline = (await db.execute(
        select(ApplicantsTimelineItem).where(ApplicantsTimelineItem.enabled.is_(True))
                                      .order_by(ApplicantsTimelineItem.sort_order, ApplicantsTimelineItem.id)
    )).scalars().all()
    docs = (await db.execute(
        select(ApplicantsDocCategory).where(ApplicantsDocCategory.enabled.is_(True))
                                     .order_by(ApplicantsDocCategory.sort_order, ApplicantsDocCategory.id)
    )).scalars().all()
    faqs = (await db.execute(
        select(ApplicantsFaq).where(ApplicantsFaq.enabled.is_(True))
                             .order_by(ApplicantsFaq.sort_order, ApplicantsFaq.id)
    )).scalars().all()

    return ApplicantsPagePublicAggregate(
        page=_page_public(page, lang),
        steps=[StepPublic(id=s.id, number=s.number, icon=s.icon,
                          title=pick(s, "title", lang) or "",
                          desc=pick(s, "desc", lang) or "") for s in steps],
        forms=[FormPublic(id=f.id,
                          title=pick(f, "title", lang) or "",
                          desc=pick(f, "desc", lang) or "",
                          features=_localize_list(f.features, lang),
                          cta_label=pick(f, "cta_label", lang),
                          cta_url=f.cta_url) for f in forms],
        timeline=[TimelinePublic(id=t.id,
                                 month=pick(t, "month", lang) or "",
                                 text=pick(t, "text", lang) or "") for t in timeline],
        docs=[DocPublic(id=d.id,
                        title=pick(d, "title", lang) or "",
                        items=_localize_list(d.items, lang)) for d in docs],
        faqs=[FaqPublic(id=q.id,
                        question=pick(q, "question", lang) or "",
                        answer=pick(q, "answer", lang) or "") for q in faqs],
    )


# ─────────────────────────────────────────────────────────────────
#  Admin
# ─────────────────────────────────────────────────────────────────
admin = APIRouter(prefix="/admin/applicants", tags=["admin:applicants"])
_dep = require_roles(Role.ADMIN, Role.CONTENT_MANAGER)


# Singleton
@admin.get("/page", response_model=ApplicantsPageAdminOut)
async def admin_get_page(
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    p = (await db.execute(select(ApplicantsPage).limit(1))).scalar_one_or_none()
    if not p:
        p = ApplicantsPage()
        db.add(p); await db.commit(); await db.refresh(p)
    return p


@admin.put("/page", response_model=ApplicantsPageAdminOut)
async def admin_update_page(
    payload: ApplicantsPageUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    p = (await db.execute(select(ApplicantsPage).limit(1))).scalar_one_or_none()
    if not p:
        p = ApplicantsPage(); db.add(p)
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(p, k, v)
    await db.commit(); await db.refresh(p)
    return p


# CRUD factory
def _crud(model, base_path: str, out_schema, create_schema, update_schema):
    @admin.get(f"/{base_path}", response_model=list[out_schema], name=f"a_list_{base_path}")
    async def _list(
        db: Annotated[AsyncSession, Depends(get_db)],
        _u: User = Depends(_dep),
    ):
        return (await db.execute(
            select(model).order_by(model.sort_order, model.id)
        )).scalars().all()

    @admin.post(f"/{base_path}", response_model=out_schema, status_code=201, name=f"a_create_{base_path}")
    async def _create(
        payload: create_schema,
        db: Annotated[AsyncSession, Depends(get_db)],
        _u: User = Depends(_dep),
    ):
        obj = model(**payload.model_dump())
        db.add(obj); await db.commit(); await db.refresh(obj)
        return obj

    @admin.put(f"/{base_path}/{{item_id}}", response_model=out_schema, name=f"a_update_{base_path}")
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

    @admin.delete(f"/{base_path}/{{item_id}}", status_code=204, name=f"a_delete_{base_path}")
    async def _delete(
        item_id: int,
        db: Annotated[AsyncSession, Depends(get_db)],
        _u: User = Depends(_dep),
    ):
        obj = await db.get(model, item_id)
        if not obj:
            raise HTTPException(404, "Not found")
        await db.delete(obj); await db.commit()


_crud(ApplicantsStep,         "steps",    StepAdminOut,     StepCreate,     StepUpdate)
_crud(ApplicantsForm,         "forms",    FormAdminOut,     FormCreate,     FormUpdate)
_crud(ApplicantsTimelineItem, "timeline", TimelineAdminOut, TimelineCreate, TimelineUpdate)
_crud(ApplicantsDocCategory,  "docs",     DocAdminOut,      DocCreate,      DocUpdate)
_crud(ApplicantsFaq,          "faqs",     FaqAdminOut,      FaqCreate,      FaqUpdate)
