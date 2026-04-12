"""
Seed about page CMS with the values previously hardcoded in AboutView.
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models.about_page import AboutPage, TimelineEvent, Accreditation


async def upsert_page(session):
    existing = (await session.execute(select(AboutPage).limit(1))).scalar_one_or_none()
    if existing:
        print("  AboutPage already seeded")
        return
    page = AboutPage(
        # Hero overrides — null = use default i18n
        hero_eyebrow_uz=None, hero_eyebrow_ru=None, hero_eyebrow_en=None,
        hero_title_uz=None,   hero_title_ru=None,   hero_title_en=None,
        hero_subtitle_uz=None, hero_subtitle_ru=None, hero_subtitle_en=None,

        # Rector
        rector_image="https://picsum.photos/seed/xiu-rector/600/750",
        rector_name_uz="Akmal Rahimov",
        rector_name_ru="Акмаль Рахимов",
        rector_name_en="Akmal Rahimov",
        rector_role_uz="Rektor",
        rector_role_ru="Ректор",
        rector_role_en="Rector",
        rector_degree_uz="Pedagogika fanlari doktori, professor",
        rector_degree_ru="Доктор педагогических наук, профессор",
        rector_degree_en="Doctor of Pedagogical Sciences, Professor",

        rector_letter_eyebrow_uz="Rektor murojaati",
        rector_letter_eyebrow_ru="Обращение ректора",
        rector_letter_eyebrow_en="Rector's message",
        rector_letter_title_uz="Bilim — eng kuchli sarmoya",
        rector_letter_title_ru="Знание — самая сильная инвестиция",
        rector_letter_title_en="Knowledge is the strongest investment",
        rector_letter_paragraphs=[
            {
                "uz": "Hurmatli abituriyent va talabalar! Xalqaro Innovatsion Universitetiga xush kelibsiz. Bizning maqsadimiz — har bir talabaga jahon darajasidagi ta'lim, zamonaviy laboratoriya va karyera imkoniyatlarini taqdim etish.",
                "ru": "Уважаемые абитуриенты и студенты! Добро пожаловать в Международный Инновационный Университет. Наша цель — предоставить каждому студенту образование мирового уровня, современные лаборатории и карьерные возможности.",
                "en": "Dear applicants and students! Welcome to the International Innovation University. Our goal is to provide every student with world-class education, modern laboratories and career opportunities."
            },
            {
                "uz": "2009 yildan beri biz minglab bitiruvchilar tarbiyalab keldik. Ularning ko'pchiligi bugungi kunda O'zbekistonning yetakchi kompaniyalarida, davlat tashkilotlarida va xalqaro hamkorlarimizda muvaffaqiyatli mehnat qilmoqda.",
                "ru": "С 2009 года мы выпустили тысячи специалистов. Многие из них сегодня успешно работают в ведущих компаниях Узбекистана, государственных учреждениях и у наших международных партнёров.",
                "en": "Since 2009 we have graduated thousands of specialists. Many of them now work successfully at Uzbekistan's leading companies, government institutions and our international partners."
            },
            {
                "uz": "XIU — bu nafaqat o'qish joyi, bu sizning shaxsiy va kasbiy o'sishingiz uchun maydon. Biz har doim sizning yoningizdamiz.",
                "ru": "XIU — это не просто место учёбы, это пространство для вашего личного и профессионального роста. Мы всегда рядом с вами.",
                "en": "XIU is not just a place to study — it's a space for your personal and professional growth. We are always by your side."
            }
        ],

        # MVV
        mvv_eyebrow_uz="Bizning yondashuv",
        mvv_eyebrow_ru="Наш подход",
        mvv_eyebrow_en="Our approach",
        mvv_title_uz="Missiya, vizyon va qadriyatlar",
        mvv_title_ru="Миссия, видение и ценности",
        mvv_title_en="Mission, vision and values",

        mission_uz="Sifatli xalqaro ta'lim orqali O'zbekistonning kelajak liderlarini tayyorlash.",
        mission_ru="Подготовка будущих лидеров Узбекистана через качественное международное образование.",
        mission_en="Preparing the future leaders of Uzbekistan through quality international education.",
        vision_uz="Markaziy Osiyodagi yetakchi xususiy universitetga aylanish.",
        vision_ru="Стать ведущим частным университетом Центральной Азии.",
        vision_en="To become Central Asia's leading private university.",
        values_uz="Bilim, halollik, innovatsiya, xalqaro hamkorlik.",
        values_ru="Знание, честность, инновации, международное сотрудничество.",
        values_en="Knowledge, integrity, innovation, international cooperation.",

        # Address / map
        address_uz="Toshkent shahar, Mirzo Ulug'bek tumani",
        address_ru="г. Ташкент, Мирзо-Улугбекский район",
        address_en="Tashkent city, Mirzo Ulugbek district",
        contact_email="info@xiuedu.uz",
        map_embed_url="https://yandex.com/map-widget/v1/?ll=69.279737%2C41.311081&z=13",
    )
    session.add(page)
    print("  AboutPage seeded")


TIMELINE = [
    dict(year="2009", title_uz="Universitet tashkil etildi", title_ru="Университет основан", title_en="University founded",
         text_uz="Toshkentda 2 fakultet bilan ish boshladi.",
         text_ru="Начал работу в Ташкенте с 2 факультетами.",
         text_en="Started in Tashkent with 2 faculties."),
    dict(year="2013", title_uz="Birinchi xalqaro hamkorlik", title_ru="Первое международное партнёрство", title_en="First international partnership",
         text_uz="Cambridge English bilan rasmiy hamkorlik shartnomasi.",
         text_ru="Официальное соглашение о сотрудничестве с Cambridge English.",
         text_en="Official partnership agreement with Cambridge English."),
    dict(year="2017", title_uz="Magistratura ochildi", title_ru="Открыта магистратура", title_en="Master's programs launched",
         text_uz="5 ta yo'nalish bo'yicha magistratura dasturlari.",
         text_ru="Запущены 5 магистерских направлений.",
         text_en="Five master's degree programs launched."),
    dict(year="2021", title_uz="Yangi kampus", title_ru="Новый кампус", title_en="New campus",
         text_uz="Zamonaviy laboratoriya va kutubxona bilan kampus ochildi.",
         text_ru="Открыт кампус с современными лабораториями и библиотекой.",
         text_en="New campus with modern labs and library opened."),
    dict(year="2026", title_uz="5000+ talaba", title_ru="5000+ студентов", title_en="5,000+ students",
         text_uz="Bugungi kunda biz O'zbekistonning yetakchi xususiy universitetimiz.",
         text_ru="Сегодня мы — один из ведущих частных университетов Узбекистана.",
         text_en="Today we are one of Uzbekistan's leading private universities."),
]


async def seed_timeline(session):
    if (await session.execute(select(TimelineEvent))).first():
        return
    for i, e in enumerate(TIMELINE):
        session.add(TimelineEvent(sort_order=i, enabled=True, **e))
    print(f"  {len(TIMELINE)} timeline events seeded")


ACCREDITATIONS = [
    dict(code="OTV",  icon="ShieldCheckIcon",
         name_uz="Oliy ta'lim vazirligi", name_ru="Министерство высшего образования", name_en="Ministry of Higher Education"),
    dict(code="ISO",  icon="AwardIcon",
         name_uz="ISO 9001",                 name_ru="ISO 9001",                       name_en="ISO 9001"),
    dict(code="ECTS", icon="GlobeAltIcon",
         name_uz="European Credit Transfer", name_ru="European Credit Transfer",       name_en="European Credit Transfer"),
    dict(code="CEFR", icon="LanguageIcon",
         name_uz="Cambridge English",        name_ru="Cambridge English",              name_en="Cambridge English"),
]


async def seed_accreditations(session):
    if (await session.execute(select(Accreditation))).first():
        return
    for i, a in enumerate(ACCREDITATIONS):
        session.add(Accreditation(sort_order=i, enabled=True, **a))
    print(f"  {len(ACCREDITATIONS)} accreditations seeded")


async def main():
    async with AsyncSessionLocal() as session:
        print("=== Seeding About page CMS ===")
        await upsert_page(session)
        await seed_timeline(session)
        await seed_accreditations(session)
        await session.commit()
        print("=== Done ===")


if __name__ == "__main__":
    asyncio.run(main())
