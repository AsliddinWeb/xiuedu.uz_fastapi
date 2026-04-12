"""Seed Structure page CMS."""
import asyncio, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models.structure_page import StructurePage, AdminDepartment, SupportService


async def upsert_page(session):
    if (await session.execute(select(StructurePage).limit(1))).scalar_one_or_none():
        print("  StructurePage already seeded"); return
    session.add(StructurePage(
        top_eyebrow_uz="Yuqori boshqaruv", top_eyebrow_ru="Высшее руководство", top_eyebrow_en="Top management",
        top_title_uz="Universitet boshqaruvi", top_title_ru="Управление университетом", top_title_en="University leadership",

        academic_eyebrow_uz="Akademik bo'linmalar", academic_eyebrow_ru="Академические подразделения", academic_eyebrow_en="Academic units",
        academic_title_uz="Fakultetlar va kafedralar",
        academic_title_ru="Факультеты и кафедры",
        academic_title_en="Faculties and departments",
        academic_lead_uz="6 ta fakultet, 21 ta kafedra va 27+ ta yo'nalish — barchasi xalqaro standartlarda.",
        academic_lead_ru="6 факультетов, 21 кафедра и более 27 направлений — всё по международным стандартам.",
        academic_lead_en="6 faculties, 21 departments and 27+ programs — all aligned with international standards.",

        admin_eyebrow_uz="Boshqaruv", admin_eyebrow_ru="Управление", admin_eyebrow_en="Administration",
        admin_title_uz="Ma'muriy bo'limlar", admin_title_ru="Административные отделы", admin_title_en="Administrative departments",
        admin_lead_uz="Universitet faoliyatini ta'minlovchi 10 ta asosiy bo'lim.",
        admin_lead_ru="10 ключевых отделов, обеспечивающих деятельность университета.",
        admin_lead_en="10 key departments that keep the university running.",

        services_eyebrow_uz="Xizmatlar", services_eyebrow_ru="Сервисы", services_eyebrow_en="Services",
        services_title_uz="Yordamchi xizmatlar", services_title_ru="Сопутствующие службы", services_title_en="Support services",
        services_lead_uz="Talabalar va xodimlar uchun zamonaviy infratuzilma.",
        services_lead_ru="Современная инфраструктура для студентов и сотрудников.",
        services_lead_en="Modern infrastructure for students and staff.",

        cta_title_uz="Qo'shimcha ma'lumot kerakmi?",
        cta_title_ru="Нужна дополнительная информация?",
        cta_title_en="Need more information?",
        cta_text_uz="Universitet tuzilmasi yoki bo'limlar haqida savollaringiz bo'lsa, biz bilan bog'laning.",
        cta_text_ru="Если у вас есть вопросы о структуре университета или подразделениях — свяжитесь с нами.",
        cta_text_en="If you have questions about the university structure or any unit, get in touch.",
        cta_primary_label_uz="Bog'lanish", cta_primary_label_ru="Связаться", cta_primary_label_en="Contact us",
        cta_primary_url="/contact",
        cta_secondary_label_uz="Universitet haqida", cta_secondary_label_ru="Об университете", cta_secondary_label_en="About the university",
        cta_secondary_url="/about",
    ))
    print("  StructurePage seeded")


DEPARTMENTS = [
    dict(icon="BookOpenIcon",        name_uz="O'quv ishlari bo'limi",  name_ru="Учебный отдел",            name_en="Academic affairs"),
    dict(icon="IdentificationIcon",  name_uz="Qabul komissiyasi",       name_ru="Приёмная комиссия",        name_en="Admissions office"),
    dict(icon="BriefcaseIcon",       name_uz="Moliya bo'limi",          name_ru="Финансовый отдел",         name_en="Finance department"),
    dict(icon="UserGroupIcon",       name_uz="Kadrlar bo'limi",         name_ru="Отдел кадров",             name_en="Human resources"),
    dict(icon="GlobeAltIcon",        name_uz="Xalqaro hamkorlik",       name_ru="Международное сотрудничество", name_en="International cooperation"),
    dict(icon="ShieldCheckIcon",     name_uz="Sifat nazorati",          name_ru="Контроль качества",        name_en="Quality assurance"),
    dict(icon="NewspaperIcon",       name_uz="Matbuot xizmati",         name_ru="Пресс-служба",             name_en="Press office"),
    dict(icon="ScaleIcon",           name_uz="Yuridik bo'lim",          name_ru="Юридический отдел",        name_en="Legal department"),
    dict(icon="ComputerDesktopIcon", name_uz="IT bo'limi",              name_ru="IT-отдел",                 name_en="IT department"),
    dict(icon="BuildingOffice2Icon", name_uz="Xo'jalik bo'limi",        name_ru="Хозяйственный отдел",      name_en="Facilities management"),
]


SERVICES = [
    dict(icon="BuildingLibraryIcon",
         name_uz="Kutubxona", name_ru="Библиотека", name_en="Library",
         desc_uz="50,000+ kitob, raqamli ma'lumotlar bazasi va sokin o'qish zonalari.",
         desc_ru="50 000+ книг, цифровая база данных и тихие зоны для чтения.",
         desc_en="50,000+ books, digital databases and quiet reading areas."),
    dict(icon="LanguageIcon",
         name_uz="Til markazi", name_ru="Языковой центр", name_en="Language centre",
         desc_uz="Cambridge English, IELTS tayyorlov va 6 ta xorijiy til kurslari.",
         desc_ru="Cambridge English, подготовка к IELTS и курсы по 6 языкам.",
         desc_en="Cambridge English, IELTS prep and courses in 6 foreign languages."),
    dict(icon="BriefcaseIcon",
         name_uz="Karyera markazi", name_ru="Карьерный центр", name_en="Career centre",
         desc_uz="Stajirovka, ishga joylashtirish va karyera maslahatlari.",
         desc_ru="Стажировки, трудоустройство и карьерное консультирование.",
         desc_en="Internships, job placement and career counselling."),
    dict(icon="BeakerIcon",
         name_uz="Ilmiy tadqiqotlar", name_ru="Научные исследования", name_en="Research",
         desc_uz="Laboratoriyalar, grantlar va xalqaro nashrlarga yordam.",
         desc_ru="Лаборатории, гранты и помощь с международными публикациями.",
         desc_en="Labs, grants and support with international publications."),
    dict(icon="BuildingOffice2Icon",
         name_uz="Yotoqxona", name_ru="Общежитие", name_en="Dormitory",
         desc_uz="Boshqa shahardan kelgan talabalar uchun zamonaviy yashash binolari.",
         desc_ru="Современные жилые корпуса для иногородних студентов.",
         desc_en="Modern residential buildings for students from other regions."),
    dict(icon="ShieldCheckIcon",
         name_uz="Tibbiy markaz", name_ru="Медицинский центр", name_en="Medical centre",
         desc_uz="Talabalar va xodimlar uchun bepul tibbiy yordam.",
         desc_ru="Бесплатная медицинская помощь для студентов и сотрудников.",
         desc_en="Free medical care for students and staff."),
]


async def seed_collection(session, model, rows, label):
    if (await session.execute(select(model))).first():
        return
    for i, r in enumerate(rows):
        session.add(model(sort_order=i, enabled=True, **r))
    print(f"  {len(rows)} {label} seeded")


async def main():
    async with AsyncSessionLocal() as session:
        print("=== Seeding Structure page ===")
        await upsert_page(session)
        await seed_collection(session, AdminDepartment, DEPARTMENTS, "departments")
        await seed_collection(session, SupportService,  SERVICES,    "services")
        await session.commit()
        print("=== Done ===")


if __name__ == "__main__":
    asyncio.run(main())
