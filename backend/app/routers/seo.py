from typing import Annotated
from xml.sax.saxutils import escape

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models.news import News
from app.models.page import StaticPage
from app.models.seo import GlobalSEO, Redirect
from app.models.user import User, Role
from app.schemas.seo import (
    GlobalSEOItem,
    GlobalSEOUpdate,
    RedirectCreate,
    RedirectOut,
    RedirectUpdate,
)
from app.utils.deps import CurrentUser, require_roles

# ===== Public =====
public = APIRouter(tags=["seo"])


SITEMAP_URLS_PER_FILE = 45000
LANGS = ("uz", "ru", "en")


def _xhtml_links(base: str, path: str) -> str:
    """Return a block of <xhtml:link rel='alternate' hreflang='..'> tags."""
    out = []
    for lg in LANGS:
        out.append(f'<xhtml:link rel="alternate" hreflang="{lg}" href="{base}{path}?lang={lg}"/>')
    out.append(f'<xhtml:link rel="alternate" hreflang="x-default" href="{base}{path}"/>')
    return "".join(out)


@public.get("/sitemap.xml", response_class=Response)
async def sitemap_index(db: Annotated[AsyncSession, Depends(get_db)]):
    """Sitemap index — splits content into per-section sub-sitemaps."""
    base = settings.SITE_URL.rstrip("/")
    parts = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for name in ("static", "pages", "news"):
        parts.append(f"<sitemap><loc>{base}/api/sitemap-{name}.xml</loc></sitemap>")
    parts.append("</sitemapindex>")
    return Response(content="\n".join(parts), media_type="application/xml")


@public.get("/sitemap-static.xml", response_class=Response)
async def sitemap_static():
    """Static URLs (homepage, sections)."""
    base = settings.SITE_URL.rstrip("/")
    routes = [
        ("/",                  "1.0", "daily"),
        ("/about",             "0.9", "monthly"),
        ("/leadership",        "0.7", "monthly"),
        ("/structure",         "0.6", "monthly"),
        ("/faculties",         "0.9", "monthly"),
        ("/education/bachelor","0.95", "monthly"),
        ("/education/master",  "0.95", "monthly"),
        ("/applicants",        "0.95", "weekly"),
        ("/students",          "0.7", "monthly"),
        ("/news",              "0.9", "daily"),
        ("/events",            "0.7", "weekly"),
        ("/gallery",           "0.6", "weekly"),
        ("/international",     "0.7", "monthly"),
        ("/contact",           "0.6", "yearly"),
        ("/careers",           "0.6", "weekly"),
    ]
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for path, prio, freq in routes:
        parts.append(
            "<url>"
            f"<loc>{base}{path}</loc>"
            f"{_xhtml_links(base, path)}"
            f"<changefreq>{freq}</changefreq><priority>{prio}</priority>"
            "</url>"
        )
    parts.append("</urlset>")
    return Response(content="\n".join(parts), media_type="application/xml")


@public.get("/sitemap-pages.xml", response_class=Response)
async def sitemap_pages(db: Annotated[AsyncSession, Depends(get_db)]):
    base = settings.SITE_URL.rstrip("/")
    rows = (
        await db.execute(select(StaticPage).where(StaticPage.is_published.is_(True)))
    ).scalars().all()

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for p in rows[:SITEMAP_URLS_PER_FILE]:
        path = f"/p/{escape(p.slug)}"
        lastmod = p.updated_at.date().isoformat() if p.updated_at else ""
        parts.append("<url>")
        parts.append(f"<loc>{base}{path}</loc>")
        parts.append(_xhtml_links(base, path))
        parts.append(f"<lastmod>{lastmod}</lastmod>")
        parts.append("<changefreq>monthly</changefreq><priority>0.8</priority>")
        if p.og_image:
            img = p.og_image if p.og_image.startswith("http") else f"{base}{p.og_image}"
            title = escape(p.title_uz or "")
            parts.append(
                f"<image:image><image:loc>{img}</image:loc>"
                f"<image:title>{title}</image:title></image:image>"
            )
        parts.append("</url>")
    parts.append("</urlset>")
    return Response(content="\n".join(parts), media_type="application/xml")


@public.get("/sitemap-news.xml", response_class=Response)
async def sitemap_news(db: Annotated[AsyncSession, Depends(get_db)]):
    base = settings.SITE_URL.rstrip("/")
    rows = (
        await db.execute(
            select(News).where(News.is_published.is_(True))
            .order_by(News.published_at.desc().nulls_last())
        )
    ).scalars().all()

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for n in rows[:SITEMAP_URLS_PER_FILE]:
        path = f"/news/{escape(n.slug)}"
        lastmod = (n.updated_at or n.published_at)
        lastmod_str = lastmod.date().isoformat() if lastmod else ""
        parts.append("<url>")
        parts.append(f"<loc>{base}{path}</loc>")
        parts.append(_xhtml_links(base, path))
        parts.append(f"<lastmod>{lastmod_str}</lastmod>")
        parts.append("<changefreq>weekly</changefreq><priority>0.7</priority>")
        if n.cover_image:
            img = n.cover_image if n.cover_image.startswith("http") else f"{base}{n.cover_image}"
            title = escape(n.title_uz or "")
            caption = escape(n.excerpt_uz or "")
            parts.append(
                "<image:image>"
                f"<image:loc>{img}</image:loc>"
                f"<image:title>{title}</image:title>"
                f"<image:caption>{caption}</image:caption>"
                "</image:image>"
            )
        parts.append("</url>")
    parts.append("</urlset>")
    return Response(content="\n".join(parts), media_type="application/xml")


@public.get("/robots.txt", response_class=PlainTextResponse)
async def robots():
    base = settings.SITE_URL.rstrip("/")
    body = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /admin/\n"
        "Disallow: /api/admin/\n"
        "Disallow: /login\n"
        "Crawl-delay: 1\n"
        "\n"
        "User-agent: GPTBot\n"
        "Disallow: /\n"
        "\n"
        f"Sitemap: {base}/api/sitemap.xml\n"
    )
    return PlainTextResponse(body)


# ===== Admin =====
admin = APIRouter(prefix="/admin/seo", tags=["admin:seo"])
_dep = require_roles(Role.ADMIN)


@admin.get("/globals", response_model=list[GlobalSEOItem])
async def list_globals(
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    rows = (await db.execute(select(GlobalSEO).order_by(GlobalSEO.key))).scalars().all()
    return rows


@admin.put("/globals/{key}", response_model=GlobalSEOItem)
async def upsert_global(
    key: str,
    payload: GlobalSEOUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    row = (
        await db.execute(select(GlobalSEO).where(GlobalSEO.key == key))
    ).scalar_one_or_none()
    if row:
        row.value = payload.value
        if payload.description is not None:
            row.description = payload.description
    else:
        row = GlobalSEO(key=key, value=payload.value, description=payload.description)
        db.add(row)
    await db.commit()
    await db.refresh(row)
    return row


@admin.get("/redirects", response_model=list[RedirectOut])
async def list_redirects(
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    rows = (await db.execute(select(Redirect).order_by(Redirect.id.desc()))).scalars().all()
    return rows


@admin.post("/redirects", response_model=RedirectOut, status_code=201)
async def create_redirect(
    payload: RedirectCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    if (
        await db.execute(select(Redirect).where(Redirect.old_path == payload.old_path))
    ).scalar_one_or_none():
        raise HTTPException(409, "old_path already exists")
    r = Redirect(**payload.model_dump())
    db.add(r)
    await db.commit()
    await db.refresh(r)
    return r


@admin.put("/redirects/{rid}", response_model=RedirectOut)
async def update_redirect(
    rid: int,
    payload: RedirectUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    r = await db.get(Redirect, rid)
    if not r:
        raise HTTPException(404, "Redirect not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(r, k, v)
    await db.commit()
    await db.refresh(r)
    return r


@admin.delete("/redirects/{rid}", status_code=204)
async def delete_redirect(
    rid: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    r = await db.get(Redirect, rid)
    if not r:
        raise HTTPException(404, "Redirect not found")
    await db.delete(r)
    await db.commit()
