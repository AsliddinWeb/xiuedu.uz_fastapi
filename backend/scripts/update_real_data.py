"""
Update ALL CMS content with real data from xiuedu.uz.
This replaces placeholder/fake values with actual university info.
"""
import asyncio, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select, update
from app.database import AsyncSessionLocal
from app.models.contact_page import ContactPage
from app.models.leader import Leader
from app.models.home_settings import (
    HeroSettings, FinalCTA, QuickAction, License, Partner, Stat
)
from app.models.about_page import AboutPage
from app.models.applicants_page import ApplicantsPage
from app.models.vacancies_page import VacanciesPage
from app.models.international_page import InternationalPage
from app.models.structure_page import StructurePage


# ═══════════════════════════════════════════════════════════════
#  REAL DATA from xiuedu.uz
# ═══════════════════════════════════════════════════════════════
PHONE = "+998 55 406-15-15"
PHONE_URL = "+998554061515"
EMAIL = "info@xiuedu.uz"
ADDRESS_UZ = "Qarshi shahri, I.Karimov ko'chasi 405-uy"
ADDRESS_RU = "г. Карши, ул. И.Каримова, дом 405"
ADDRESS_EN = "Qarshi city, I. Karimov Street, Building 405"
HOURS_UZ = "Du-Ju: 09:00-18:00, Sha-Ya: 10:30-17:00"
HOURS_RU = "Пн-Пт: 09:00-18:00, Сб-Вс: 10:30-17:00"
HOURS_EN = "Mon-Fri: 09:00-18:00, Sat-Sun: 10:30-17:00"
ADMISSION_URL = "https://qabul.xiuedu.uz"
HEMIS_URL = "https://student.xiuedu.uz"

RECTOR_NAME_UZ = "Madiyev Otamurod Bobomurodovich"
RECTOR_NAME_RU = "Мадиев Отамурод Бобомуродович"
RECTOR_NAME_EN = "Madiyev Otamurod Bobomurodovich"

# Real social media
TELEGRAM = "https://t.me/xalqaro_innovatsion_universiteti"
INSTAGRAM = "https://www.instagram.com/xiu_edu.uz"
FACEBOOK = "https://www.facebook.com/profile.php?id=100090241119598"
YOUTUBE = "https://www.youtube.com/@xiu_youtube"


async def main():
    async with AsyncSessionLocal() as session:
        print("=== Updating real data ===")

        # ── Contact page ──
        contact = (await session.execute(select(ContactPage).limit(1))).scalar_one_or_none()
        if contact:
            contact.address_uz = ADDRESS_UZ
            contact.address_ru = ADDRESS_RU
            contact.address_en = ADDRESS_EN
            contact.phone = PHONE
            contact.email = EMAIL
            contact.working_hours_uz = HOURS_UZ
            contact.working_hours_ru = HOURS_RU
            contact.working_hours_en = HOURS_EN
            print("  ✓ ContactPage updated")

        # ── About page ──
        about = (await session.execute(select(AboutPage).limit(1))).scalar_one_or_none()
        if about:
            about.rector_name_uz = RECTOR_NAME_UZ
            about.rector_name_ru = RECTOR_NAME_RU
            about.rector_name_en = RECTOR_NAME_EN
            about.rector_role_uz = "Rektor"
            about.rector_role_ru = "Ректор"
            about.rector_role_en = "Rector"
            about.rector_degree_uz = "Iqtisodiyot fanlari nomzodi"
            about.rector_degree_ru = "Кандидат экономических наук"
            about.rector_degree_en = "PhD in Economics"
            about.address_uz = ADDRESS_UZ
            about.address_ru = ADDRESS_RU
            about.address_en = ADDRESS_EN
            about.contact_email = EMAIL
            print("  ✓ AboutPage updated")

        # ── Leaders (rector) ──
        rector = (await session.execute(
            select(Leader).where(Leader.group == "rector")
        )).scalar_one_or_none()
        if rector:
            rector.name_uz = RECTOR_NAME_UZ
            rector.name_ru = RECTOR_NAME_RU
            rector.name_en = RECTOR_NAME_EN
            rector.degree_uz = "Iqtisodiyot fanlari nomzodi"
            rector.degree_ru = "Кандидат экономических наук"
            rector.degree_en = "PhD in Economics"
            rector.email = "rektor@xiuedu.uz"
            rector.phone = PHONE
            print("  ✓ Leader (rector) updated")

        # ── Leaders (prorectors — real names) ──
        prorectors = (await session.execute(
            select(Leader).where(Leader.group == "prorector").order_by(Leader.sort_order)
        )).scalars().all()
        real_prorectors = [
            {
                "name_uz": "Jabborov Jamshid Azimovich",
                "name_ru": "Жабборов Жамшид Азимович",
                "name_en": "Jabborov Jamshid Azimovich",
                "position_uz": "Yoshlar va ma'naviyat masalalari bo'yicha prorektor",
                "position_ru": "Проректор по делам молодёжи и духовности",
                "position_en": "Vice-rector for youth and spiritual affairs",
            },
            {
                "name_uz": "Haydarov Toshtemir Navruzovich",
                "name_ru": "Хайдаров Тоштемир Наврузович",
                "name_en": "Haydarov Toshtemir Navruzovich",
                "position_uz": "O'quv ishlari bo'yicha prorektor",
                "position_ru": "Проректор по учебной работе",
                "position_en": "Vice-rector for academic affairs",
            },
        ]
        for i, data in enumerate(real_prorectors):
            if i < len(prorectors):
                for k, v in data.items():
                    setattr(prorectors[i], k, v)
        print(f"  ✓ {min(len(real_prorectors), len(prorectors))} prorectors updated")

        # ── Home hero ──
        hero = (await session.execute(
            select(HeroSettings).where(HeroSettings.page == "home")
        )).scalar_one_or_none()
        if hero:
            hero.cta_primary_url = ADMISSION_URL
            print("  ✓ Hero CTA URL updated")

        # ── Final CTA ──
        cta = (await session.execute(select(FinalCTA).limit(1))).scalar_one_or_none()
        if cta:
            cta.cta_url = ADMISSION_URL
            cta.phone_label = PHONE
            cta.phone_url = PHONE_URL
            print("  ✓ FinalCTA updated")

        # ── Quick Actions (admission + HEMIS) ──
        qas = (await session.execute(select(QuickAction))).scalars().all()
        for qa in qas:
            if "admission" in (qa.url or "").lower() or qa.accent:
                qa.url = ADMISSION_URL
            elif "student" in (qa.url or "").lower():
                qa.url = HEMIS_URL
        print("  ✓ QuickActions URLs updated")

        # ── Applicants page CTA ──
        app_page = (await session.execute(select(ApplicantsPage).limit(1))).scalar_one_or_none()
        if app_page:
            app_page.cta_primary_url = ADMISSION_URL
            app_page.cta_phone_label = PHONE
            app_page.cta_phone_url = PHONE_URL
            print("  ✓ ApplicantsPage CTA updated")

        # ── Vacancies page ──
        vac_page = (await session.execute(select(VacanciesPage).limit(1))).scalar_one_or_none()
        if vac_page:
            vac_page.cv_email = "hr@xiuedu.uz"
            print("  ✓ VacanciesPage email updated")

        # ── International page ──
        intl = (await session.execute(select(InternationalPage).limit(1))).scalar_one_or_none()
        if intl:
            intl.cta_email = "international@xiuedu.uz"
            intl.cta_phone_label = PHONE
            intl.cta_phone_url = PHONE_URL
            print("  ✓ InternationalPage contact updated")

        # ── Structure CTA ──
        struct = (await session.execute(select(StructurePage).limit(1))).scalar_one_or_none()
        if struct:
            struct.cta_primary_url = "/contact"
            struct.cta_secondary_url = "/about"
            print("  ✓ StructurePage CTA updated")

        # ── Licenses — update with real license ──
        licenses = (await session.execute(select(License).order_by(License.sort_order))).scalars().all()
        if licenses:
            licenses[0].title_uz = "Davlat ta'lim litsenziyasi №222829"
            licenses[0].title_ru = "Государственная лицензия на образование №222829"
            licenses[0].title_en = "State education licence No. 222829"
            licenses[0].issuer_uz = "Vazirlar Mahkamasi huzuridagi Ta'lim sifatini nazorat qilish davlat inspeksiyasi"
            licenses[0].issuer_ru = "Государственная инспекция по контролю качества образования при Кабинете Министров"
            licenses[0].issuer_en = "State Inspection for Quality Control of Education under the Cabinet of Ministers"
            licenses[0].year = 2022
            print("  ✓ License #1 updated with real data")

        # ── Stats — update to real numbers ──
        stats = (await session.execute(select(Stat).order_by(Stat.sort_order))).scalars().all()
        real_stats = [
            {"value": "4200+", "label_uz": "Talabalar", "label_ru": "Студентов", "label_en": "Students",
             "sub_uz": "Kunduzgi va sirtqi", "sub_ru": "Очная и заочная формы", "sub_en": "Full-time and part-time"},
            {"value": "86+", "label_uz": "Ilmiy daraja ega o'qituvchilar", "label_ru": "Преподавателей с научной степенью", "label_en": "Faculty with scientific degrees",
             "sub_uz": "Professor-o'qituvchilar", "sub_ru": "Профессорско-преподавательский состав", "sub_en": "Academic staff"},
            {"value": "20+", "label_uz": "Bakalavr yo'nalishlari", "label_ru": "Направлений бакалавриата", "label_en": "Bachelor programs",
             "sub_uz": "Barcha fakultetlar", "sub_ru": "Все факультеты", "sub_en": "All faculties"},
            {"value": "3", "label_uz": "Fakultet", "label_ru": "Факультета", "label_en": "Faculties",
             "sub_uz": "Pedagogika, Iqtisodiyot, Filologiya", "sub_ru": "Педагогика, Экономика, Филология", "sub_en": "Pedagogy, Economics, Philology"},
        ]
        for i, data in enumerate(real_stats):
            if i < len(stats):
                for k, v in data.items():
                    setattr(stats[i], k, v)
        print(f"  ✓ {min(len(real_stats), len(stats))} stats updated")

        await session.commit()
        print("=== Done ===")


if __name__ == "__main__":
    asyncio.run(main())
