"""Seed Gallery page CMS with categories + placeholder items."""
import asyncio, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models.gallery_page import GalleryPage, GalleryCategory, GalleryItem

CATS = [
    dict(slug="event",   name_uz="Tadbirlar",  name_ru="Мероприятия", name_en="Events"),
    dict(slug="student", name_uz="Talabalar",  name_ru="Студенты",   name_en="Students"),
    dict(slug="sport",   name_uz="Sport",      name_ru="Спорт",      name_en="Sport"),
    dict(slug="campus",  name_uz="Binolar",    name_ru="Здания",     name_en="Buildings"),
]


async def main():
    async with AsyncSessionLocal() as session:
        # Page singleton
        if not (await session.execute(select(GalleryPage).limit(1))).scalar_one_or_none():
            session.add(GalleryPage())
            print("  GalleryPage seeded")

        # Categories
        if (await session.execute(select(GalleryCategory))).first():
            print("  Categories already seeded")
        else:
            for i, c in enumerate(CATS):
                cat = GalleryCategory(sort_order=i, enabled=True, **c)
                session.add(cat)
            await session.flush()
            print(f"  {len(CATS)} categories seeded")

            # Seed 5 placeholder items per category
            cats = (await session.execute(
                select(GalleryCategory).order_by(GalleryCategory.id)
            )).scalars().all()
            count = 0
            for cat in cats:
                for j in range(5):
                    session.add(GalleryItem(
                        category_id=cat.id,
                        sort_order=j,
                        enabled=True,
                        image=f"https://picsum.photos/seed/xiu-gallery-{cat.slug}-{j}/800/600",
                        caption_uz=f"{cat.name_uz} #{j+1}",
                        caption_ru=f"{cat.name_ru} #{j+1}",
                        caption_en=f"{cat.name_en} #{j+1}",
                        alt_uz=f"{cat.name_uz} rasmi",
                        alt_ru=f"Фото {cat.name_ru}",
                        alt_en=f"{cat.name_en} photo",
                    ))
                    count += 1
            print(f"  {count} gallery items seeded")

        await session.commit()
        print("=== Done ===")


if __name__ == "__main__":
    asyncio.run(main())
