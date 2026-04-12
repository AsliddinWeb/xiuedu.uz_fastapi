"""Seed Vacancies page CMS."""
import asyncio, os, sys
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models.vacancies_page import VacanciesPage, Vacancy


async def upsert_page(session):
    if (await session.execute(select(VacanciesPage).limit(1))).scalar_one_or_none():
        print("  VacanciesPage already seeded"); return
    session.add(VacanciesPage(
        hero_eyebrow_uz="Karyera", hero_eyebrow_ru="Карьера", hero_eyebrow_en="Careers",
        hero_title_uz="Vakansiyalar", hero_title_ru="Вакансии", hero_title_en="Vacancies",
        hero_subtitle_uz="XIU Edu jamoasiga qo'shiling — birga o'sing va ta'lim sohasini rivojlantiring.",
        hero_subtitle_ru="Присоединяйтесь к команде XIU Edu — растите вместе с нами и развивайте сферу образования.",
        hero_subtitle_en="Join the XIU Edu team — grow with us and shape the future of education.",

        empty_title_uz="Hozircha bo'sh ish o'rni yo'q",
        empty_title_ru="Сейчас нет открытых вакансий",
        empty_title_en="No open positions right now",
        empty_text_uz="Yangi vakansiyalar paydo bo'lganda bu yerda e'lon qilamiz.",
        empty_text_ru="Когда появятся новые вакансии, мы опубликуем их здесь.",
        empty_text_en="We'll post new openings here when they become available.",

        cv_title_uz="CV yuborish",
        cv_title_ru="Отправить резюме",
        cv_title_en="Send your CV",
        cv_text_uz="Mos vakansiya yo'qmi? CV ni yuboring va biz mos imkoniyat paydo bo'lganda bog'lanamiz.",
        cv_text_ru="Не нашли подходящую вакансию? Отправьте нам резюме, и мы свяжемся, когда появится возможность.",
        cv_text_en="Don't see a fitting role? Send us your CV and we'll reach out when there's a match.",
        cv_email="hr@xiuedu.uz",
    ))
    print("  VacanciesPage seeded")


VACANCIES = [
    dict(
        is_open=True,
        title_uz="Ingliz tili o'qituvchisi",
        title_ru="Преподаватель английского языка",
        title_en="English language teacher",
        department_uz="Filologiya fakulteti",
        department_ru="Филологический факультет",
        department_en="Faculty of Philology",
        employment_type="full_time",
        location_uz="Toshkent", location_ru="Ташкент", location_en="Tashkent",
        description_uz="Akademik daraja IELTS 7.5+ talab qilinadi. Cambridge English bilan ishlash tajribasi afzallik.",
        description_ru="Требуется уровень IELTS 7.5+. Опыт работы с Cambridge English будет преимуществом.",
        description_en="IELTS 7.5+ required. Experience with Cambridge English programs is a plus.",
        requirements_uz="• Magistr darajasi\n• 3+ yil tajriba\n• IELTS 7.5+",
        requirements_ru="• Степень магистра\n• Опыт от 3 лет\n• IELTS 7.5+",
        requirements_en="• Master's degree\n• 3+ years experience\n• IELTS 7.5+",
        salary="8-12 mln so'm",
        contact_email="hr@xiuedu.uz",
        posted_at=date.today() - timedelta(days=5),
        deadline=date.today() + timedelta(days=25),
    ),
    dict(
        is_open=True,
        title_uz="Marketing kafedrasi assistenti",
        title_ru="Ассистент кафедры маркетинга",
        title_en="Marketing department assistant",
        department_uz="Iqtisodiyot fakulteti",
        department_ru="Экономический факультет",
        department_en="Faculty of Economics",
        employment_type="full_time",
        location_uz="Toshkent", location_ru="Ташкент", location_en="Tashkent",
        description_uz="Marketing yo'nalishida bakalavr darajasi va o'qitish istagi.",
        description_ru="Степень бакалавра по маркетингу и желание преподавать.",
        description_en="Bachelor's in marketing and willingness to teach.",
        requirements_uz="• Bakalavr darajasi\n• Ingliz tili B2+\n• Pedagogik tajriba afzallik",
        requirements_ru="• Степень бакалавра\n• Английский B2+\n• Опыт преподавания приветствуется",
        requirements_en="• Bachelor's degree\n• English B2+\n• Teaching experience preferred",
        salary="6-9 mln so'm",
        contact_email="hr@xiuedu.uz",
        posted_at=date.today() - timedelta(days=7),
        deadline=date.today() + timedelta(days=20),
    ),
    dict(
        is_open=True,
        title_uz="IT mutaxassisi",
        title_ru="IT-специалист",
        title_en="IT specialist",
        department_uz="Axborot xizmati",
        department_ru="Информационная служба",
        department_en="IT department",
        employment_type="full_time",
        location_uz="Toshkent", location_ru="Ташкент", location_en="Tashkent",
        description_uz="Universitet IT infratuzilmasini qo'llab-quvvatlash. Linux/Windows tajriba.",
        description_ru="Поддержка IT-инфраструктуры университета. Опыт Linux/Windows.",
        description_en="Maintain university IT infrastructure. Linux/Windows experience.",
        requirements_uz="• Bakalavr (IT/CS)\n• Linux/Windows admin\n• Tarmoq bilim",
        requirements_ru="• Бакалавр (IT/CS)\n• Linux/Windows админ\n• Знание сетей",
        requirements_en="• Bachelor's (IT/CS)\n• Linux/Windows admin\n• Networking knowledge",
        salary="9-14 mln so'm",
        contact_email="hr@xiuedu.uz",
        posted_at=date.today() - timedelta(days=14),
        deadline=date.today() + timedelta(days=15),
    ),
]


async def seed_vacancies(session):
    if (await session.execute(select(Vacancy))).first():
        return
    for i, v in enumerate(VACANCIES):
        session.add(Vacancy(sort_order=i, enabled=True, **v))
    print(f"  {len(VACANCIES)} vacancies seeded")


async def main():
    async with AsyncSessionLocal() as session:
        print("=== Seeding Vacancies page ===")
        await upsert_page(session)
        await seed_vacancies(session)
        await session.commit()
        print("=== Done ===")


if __name__ == "__main__":
    asyncio.run(main())
