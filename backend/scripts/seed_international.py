"""Seed International page CMS."""
import asyncio, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models.international_page import InternationalPage, IntlProgram, IntlPartner


async def upsert_page(session):
    if (await session.execute(select(InternationalPage).limit(1))).scalar_one_or_none():
        print("  InternationalPage already seeded"); return
    session.add(InternationalPage(
        hero_eyebrow_uz="Xalqaro hamkorlik", hero_eyebrow_ru="Международное сотрудничество", hero_eyebrow_en="International cooperation",
        hero_title_uz="Dunyoning yetakchi universitetlari bilan birga",
        hero_title_ru="Вместе с ведущими университетами мира",
        hero_title_en="Together with the world's leading universities",
        hero_subtitle_uz="50+ partner, 15 mamlakat va o'nlab xalqaro dasturlar.",
        hero_subtitle_ru="50+ партнёров, 15 стран и десятки международных программ.",
        hero_subtitle_en="50+ partners, 15 countries and dozens of international programs.",

        # Stats
        stat1_value="50+",
        stat1_label_uz="Hamkor universitet",  stat1_label_ru="Партнёров",        stat1_label_en="Partner universities",
        stat2_value="15",
        stat2_label_uz="Mamlakat",            stat2_label_ru="Стран",             stat2_label_en="Countries",
        stat3_value="120+",
        stat3_label_uz="Almashinuv talabalari", stat3_label_ru="Студентов по обмену", stat3_label_en="Exchange students",
        stat4_value="8",
        stat4_label_uz="Dual dastur",         stat4_label_ru="Двойных программ",  stat4_label_en="Dual programs",

        programs_eyebrow_uz="Dasturlar",      programs_eyebrow_ru="Программы",     programs_eyebrow_en="Programs",
        programs_title_uz="Xalqaro imkoniyatlar",
        programs_title_ru="Международные возможности",
        programs_title_en="International opportunities",

        partners_eyebrow_uz="Hamkorlar",      partners_eyebrow_ru="Партнёры",      partners_eyebrow_en="Partners",
        partners_title_uz="Bizning xalqaro hamkorlar",
        partners_title_ru="Наши международные партнёры",
        partners_title_en="Our international partners",

        cta_title_uz="Xalqaro bo'lim",        cta_title_ru="Международный отдел",  cta_title_en="International office",
        cta_text_uz="Hamkorlik, almashinuv va xalqaro dasturlar bo'yicha murojaat qiling.",
        cta_text_ru="Свяжитесь с нами по вопросам сотрудничества, обменов и международных программ.",
        cta_text_en="Contact us regarding partnerships, exchanges and international programs.",
        cta_email="international@xiuedu.uz",
        cta_phone_label="+998 55 406-15-15",
        cta_phone_url="+998554061515",
    ))
    print("  InternationalPage seeded")


PROGRAMS = [
    dict(icon="PaperAirplaneIcon",
         title_uz="Almashinuv dasturlari", title_ru="Программы обмена", title_en="Exchange programs",
         desc_uz="1–2 semestr xorijiy universitetda ta'lim olish.",
         desc_ru="Обучение в зарубежном университете 1–2 семестра.",
         desc_en="Study at a foreign university for 1-2 semesters."),
    dict(icon="StarIcon",
         title_uz="Dual diploma", title_ru="Двойной диплом", title_en="Dual degree",
         desc_uz="Bir vaqtda ikki universitetdan diplom oling.",
         desc_ru="Получите дипломы двух университетов одновременно.",
         desc_en="Earn diplomas from two universities at once."),
    dict(icon="UserGroupIcon",
         title_uz="Xalqaro stajirovkalar", title_ru="Международные стажировки", title_en="International internships",
         desc_uz="Yetakchi kompaniyalarda yozgi amaliyot.",
         desc_ru="Летние стажировки в ведущих компаниях.",
         desc_en="Summer internships at leading companies."),
    dict(icon="BeakerIcon",
         title_uz="Qo'shma tadqiqotlar", title_ru="Совместные исследования", title_en="Joint research",
         desc_uz="Xalqaro ilmiy loyihalarda ishtirok eting.",
         desc_ru="Участвуйте в международных научных проектах.",
         desc_en="Join international research projects."),
]


PARTNERS = [
    ("Cambridge English",  "GB", "🇬🇧"),
    ("Oxford University",  "GB", "🇬🇧"),
    ("Sorbonne",           "FR", "🇫🇷"),
    ("TU Berlin",          "DE", "🇩🇪"),
    ("KAIST",              "KR", "🇰🇷"),
    ("ETH Zurich",         "CH", "🇨🇭"),
    ("Bocconi",            "IT", "🇮🇹"),
    ("NUS",                "SG", "🇸🇬"),
    ("McGill",             "CA", "🇨🇦"),
    ("KU Leuven",          "BE", "🇧🇪"),
    ("Lund University",    "SE", "🇸🇪"),
    ("Tsinghua",           "CN", "🇨🇳"),
]


async def seed_programs(session):
    if (await session.execute(select(IntlProgram))).first():
        return
    for i, p in enumerate(PROGRAMS):
        session.add(IntlProgram(sort_order=i, enabled=True, **p))
    print(f"  {len(PROGRAMS)} programs seeded")


async def seed_partners(session):
    if (await session.execute(select(IntlPartner))).first():
        return
    for i, (name, code, flag) in enumerate(PARTNERS):
        session.add(IntlPartner(sort_order=i, enabled=True, name=name, country_code=code, flag=flag))
    print(f"  {len(PARTNERS)} partners seeded")


async def main():
    async with AsyncSessionLocal() as session:
        print("=== Seeding International page ===")
        await upsert_page(session)
        await seed_programs(session)
        await seed_partners(session)
        await session.commit()
        print("=== Done ===")


if __name__ == "__main__":
    asyncio.run(main())
