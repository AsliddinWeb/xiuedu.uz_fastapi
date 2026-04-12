"""Seed Contact page CMS."""
import asyncio, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models.contact_page import ContactPage


async def main():
    async with AsyncSessionLocal() as session:
        if (await session.execute(select(ContactPage).limit(1))).scalar_one_or_none():
            print("ContactPage already seeded"); return
        session.add(ContactPage(
            address_uz="Toshkent shahar, Mirzo Ulug'bek tumani",
            address_ru="г. Ташкент, Мирзо-Улугбекский район",
            address_en="Tashkent city, Mirzo Ulugbek district",
            phone="+998 55 406-15-15",
            email="info@xiuedu.uz",
            working_hours_uz="Du-Ju: 09:00 — 18:00",
            working_hours_ru="Пн-Пт: 09:00 — 18:00",
            working_hours_en="Mon-Fri: 09:00 — 18:00",
            form_title_uz="Bizga yozing",
            form_title_ru="Напишите нам",
            form_title_en="Write to us",
            form_subtitle_uz="Savollaringizga 24 soat ichida javob beramiz.",
            form_subtitle_ru="Ответим на ваши вопросы в течение 24 часов.",
            form_subtitle_en="We'll respond to your questions within 24 hours.",
            map_embed_url="https://yandex.com/map-widget/v1/?ll=69.279737%2C41.311081&z=13",
        ))
        await session.commit()
        print("ContactPage seeded")


if __name__ == "__main__":
    asyncio.run(main())
