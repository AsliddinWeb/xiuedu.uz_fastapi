"""
Seed initial data for a fresh XIU Edu v2 install.

Usage:
    docker compose exec backend python scripts/seed_data.py
"""
import asyncio
import os
import sys
from datetime import datetime, timezone

# Make app importable when run from /app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select

from app.config import settings
from app.database import AsyncSessionLocal
from app.models.news import News, NewsCategory
from app.models.page import StaticPage
from app.models.seo import GlobalSEO
from app.models.user import Role, User
from app.utils.security import hash_password


async def get_or_create(session, model, defaults=None, **lookup):
    obj = (await session.execute(select(model).filter_by(**lookup))).scalar_one_or_none()
    if obj:
        return obj, False
    obj = model(**lookup, **(defaults or {}))
    session.add(obj)
    await session.flush()
    return obj, True


async def seed_users(session):
    print("Seeding superadmin...")
    user, created = await get_or_create(
        session, User, email=settings.ADMIN_EMAIL,
        defaults={
            "hashed_password": hash_password(settings.ADMIN_PASSWORD),
            "full_name": "Super Admin",
            "role": Role.SUPERADMIN,
            "is_active": True,
            "is_verified": True,
        },
    )
    print("  ", "created" if created else "exists", user.email)
    return user


async def seed_categories(session):
    print("Seeding news categories...")
    cats = [
        ("yangiliklar", "Yangiliklar",  "Новости",     "News",        "#0B1F4B", "newspaper"),
        ("tadbirlar",   "Tadbirlar",    "События",     "Events",      "#D4AF37", "calendar"),
        ("ilm-fan",     "Ilm-fan",      "Наука",       "Science",     "#0EA5E9", "flask-conical"),
        ("xalqaro",     "Xalqaro",      "Международ.", "International","#16A34A", "globe-2"),
    ]
    out = {}
    for slug, uz, ru, en, color, icon in cats:
        c, created = await get_or_create(
            session, NewsCategory, slug=slug,
            defaults={"name_uz": uz, "name_ru": ru, "name_en": en, "color": color, "icon": icon},
        )
        out[slug] = c
        print("  ", "+" if created else "=", slug)
    return out


async def seed_pages(session, author):
    print("Seeding static pages...")
    pages = [
        ("about",            "Biz haqimizda",   "О нас",        "About"),
        ("leadership-text",  "Rahbariyat",      "Руководство",  "Leadership"),
        ("tarkibiy-tuzilma", "Tarkibiy tuzilma","Структура",    "Structure"),
        ("xalqaro-hamkorlik","Xalqaro hamkorlik","Международное сотрудничество", "International cooperation"),
        ("vakansiyalar",     "Vakansiyalar",    "Вакансии",     "Careers"),
        ("documents",        "Hujjatlar",       "Документы",    "Documents"),
        ("privacy",          "Maxfiylik siyosati","Политика конфиденциальности","Privacy policy"),
        ("terms",            "Foydalanish shartlari","Условия использования","Terms of use"),
    ]
    for slug, uz, ru, en in pages:
        await get_or_create(
            session, StaticPage, slug=slug,
            defaults={
                "title_uz": uz, "title_ru": ru, "title_en": en,
                "content_uz": f"<p>{uz} sahifasi tayyorlanmoqda.</p>",
                "content_ru": f"<p>Страница «{ru}» в подготовке.</p>",
                "content_en": f"<p>{en} page coming soon.</p>",
                "is_published": True,
                "created_by": author.id,
            },
        )
        print("  +", slug)


async def seed_news(session, cats, author):
    print("Seeding sample news...")
    samples = [
        ("xush-kelibsiz-yangi-veb-saytga", "yangiliklar",
         "Xush kelibsiz! Yangi XIU Edu sayti", "Добро пожаловать! Новый сайт XIU Edu", "Welcome! The new XIU Edu site"),
        ("ochiq-eshiklar-kuni-2026", "tadbirlar",
         "Ochiq eshiklar kuni 2026", "День открытых дверей 2026", "Open doors day 2026"),
        ("xalqaro-hamkorlik-cambridge", "xalqaro",
         "Cambridge English bilan yangi shartnoma", "Новое соглашение с Cambridge English", "New Cambridge English agreement"),
        ("ilmiy-konferensiya-2026", "ilm-fan",
         "Talabalar ilmiy konferensiyasi 2026", "Студенческая научная конференция 2026", "Students' scientific conference 2026"),
        ("akkreditatsiya-yangilandi", "yangiliklar",
         "Akkreditatsiya yangilandi", "Аккредитация продлена", "Accreditation renewed"),
    ]
    now = datetime.now(timezone.utc)
    for slug, cat_slug, uz, ru, en in samples:
        cat = cats.get(cat_slug)
        await get_or_create(
            session, News, slug=slug,
            defaults={
                "title_uz": uz, "title_ru": ru, "title_en": en,
                "excerpt_uz": uz, "excerpt_ru": ru, "excerpt_en": en,
                "body_uz": f"<p>{uz}.</p><p>Batafsil ma'lumot keyinroq qo'shiladi.</p>",
                "body_ru": f"<p>{ru}.</p>",
                "body_en": f"<p>{en}.</p>",
                "is_published": True,
                "is_featured": cat_slug in ("yangiliklar", "tadbirlar"),
                "category_id": cat.id if cat else None,
                "author_id": author.id,
                "published_at": now,
                "gallery": [],
            },
        )
        print("  +", slug)


async def seed_seo(session):
    print("Seeding global SEO defaults...")
    items = [
        ("site_title_template",     "%s | XIU Edu", "Site title template"),
        ("default_description_uz",  "Xalqaro Innovatsion Universiteti — O'zbekistondagi yetakchi xususiy universitet.", ""),
        ("default_description_ru",  "Международный Инновационный Университет — ведущий частный университет Узбекистана.", ""),
        ("default_description_en",  "International Innovation University — Uzbekistan's leading private university.", ""),
        ("default_og_image",        "/og-image.jpg", ""),
        ("google_analytics_id",     "", "GA4 measurement ID"),
        ("yandex_metrica_id",       "", "Yandex Metrica counter ID"),
    ]
    for key, value, desc in items:
        await get_or_create(
            session, GlobalSEO, key=key,
            defaults={"value": value, "description": desc},
        )
        print("  +", key)


async def main():
    async with AsyncSessionLocal() as session:
        admin = await seed_users(session)
        cats = await seed_categories(session)
        await seed_pages(session, admin)
        await seed_news(session, cats, admin)
        await seed_seo(session)
        await session.commit()
    print("\n✅ Seed complete.")
    print(f"   Admin: {settings.ADMIN_EMAIL} / {settings.ADMIN_PASSWORD}")


if __name__ == "__main__":
    asyncio.run(main())
