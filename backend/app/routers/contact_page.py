"""Contact page singleton — public GET + admin GET/PUT."""
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.contact_page import ContactPage
from app.models.user import Role, User
from app.schemas.contact_page import ContactPageAdminOut, ContactPagePublic, ContactPageUpdate
from app.utils.deps import require_roles
from app.utils.lang import Lang, get_lang, pick

# ── Public ──
public = APIRouter(prefix="/page-settings", tags=["page-settings:contact"])


@public.get("/contact", response_model=ContactPagePublic)
async def get_contact(
    db: Annotated[AsyncSession, Depends(get_db)],
    lang: Annotated[Lang, Depends(get_lang)],
):
    p = (await db.execute(select(ContactPage).limit(1))).scalar_one_or_none()
    if not p:
        return ContactPagePublic(
            hero_eyebrow=None, hero_title=None, hero_subtitle=None,
            address=None, phone=None, email=None, working_hours=None,
            form_title=None, form_subtitle=None, map_embed_url=None,
        )
    return ContactPagePublic(
        hero_eyebrow=pick(p, "hero_eyebrow", lang),
        hero_title=pick(p, "hero_title", lang),
        hero_subtitle=pick(p, "hero_subtitle", lang),
        address=pick(p, "address", lang),
        phone=p.phone,
        email=p.email,
        working_hours=pick(p, "working_hours", lang),
        form_title=pick(p, "form_title", lang),
        form_subtitle=pick(p, "form_subtitle", lang),
        map_embed_url=p.map_embed_url,
    )


# ── Admin ──
admin = APIRouter(prefix="/admin/contact", tags=["admin:contact"])
_dep = require_roles(Role.ADMIN, Role.CONTENT_MANAGER)


@admin.get("/page", response_model=ContactPageAdminOut)
async def admin_get(
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    p = (await db.execute(select(ContactPage).limit(1))).scalar_one_or_none()
    if not p:
        p = ContactPage()
        db.add(p); await db.commit(); await db.refresh(p)
    return p


@admin.put("/page", response_model=ContactPageAdminOut)
async def admin_update(
    payload: ContactPageUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    p = (await db.execute(select(ContactPage).limit(1))).scalar_one_or_none()
    if not p:
        p = ContactPage(); db.add(p)
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(p, k, v)
    await db.commit(); await db.refresh(p)
    return p
