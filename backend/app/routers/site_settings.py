"""Site settings — public GET + admin GET/PUT."""
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.site_settings import SiteSettings
from app.models.user import Role, User
from app.schemas.site_settings import SiteSettingsAdminOut, SiteSettingsPublic, SiteSettingsUpdate
from app.utils.deps import require_roles
from app.utils.lang import Lang, get_lang, pick

public = APIRouter(prefix="/site-settings", tags=["site-settings"])


@public.get("/", response_model=SiteSettingsPublic)
async def get_site_settings(
    db: Annotated[AsyncSession, Depends(get_db)],
    lang: Annotated[Lang, Depends(get_lang)],
):
    s = (await db.execute(select(SiteSettings).limit(1))).scalar_one_or_none()
    if not s:
        return SiteSettingsPublic(
            site_name=None, site_short_name=None, logo_url=None, logo_dark_url=None,
            favicon_url=None, og_image_url=None,
            brand_line1=None, brand_line2=None,
            footer_desc=None,
            telegram_url=None, instagram_url=None, facebook_url=None, youtube_url=None,
            phone=None, email=None, address=None, hemis_url=None, admission_url=None,
        )
    return SiteSettingsPublic(
        site_name=pick(s, "site_name", lang),
        site_short_name=s.site_short_name,
        logo_url=s.logo_url,
        logo_dark_url=s.logo_dark_url,
        favicon_url=s.favicon_url,
        og_image_url=s.og_image_url,
        brand_line1=pick(s, "brand_line1", lang),
        brand_line2=pick(s, "brand_line2", lang),
        footer_desc=pick(s, "footer_desc", lang),
        telegram_url=s.telegram_url,
        instagram_url=s.instagram_url,
        facebook_url=s.facebook_url,
        youtube_url=s.youtube_url,
        phone=s.phone,
        email=s.email,
        address=pick(s, "address", lang),
        hemis_url=s.hemis_url,
        admission_url=s.admission_url,
    )


admin = APIRouter(prefix="/admin/site-settings", tags=["admin:site-settings"])
_dep = require_roles(Role.ADMIN)


@admin.get("/", response_model=SiteSettingsAdminOut)
async def admin_get(
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    s = (await db.execute(select(SiteSettings).limit(1))).scalar_one_or_none()
    if not s:
        s = SiteSettings()
        db.add(s); await db.commit(); await db.refresh(s)
    return s


@admin.put("/", response_model=SiteSettingsAdminOut)
async def admin_update(
    payload: SiteSettingsUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    s = (await db.execute(select(SiteSettings).limit(1))).scalar_one_or_none()
    if not s:
        s = SiteSettings(); db.add(s)
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(s, k, v)
    await db.commit(); await db.refresh(s)
    return s
