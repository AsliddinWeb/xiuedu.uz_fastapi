"""
Seed home page CMS content with the same values currently hardcoded
in HomeView.vue.

Usage:
    docker compose exec backend python scripts/seed_home.py
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select, delete

from app.database import AsyncSessionLocal
from app.models.home_settings import (
    HeroSettings, HomeSection, QuickAction, IntroPillar, CampusSection,
    WhyCard, Faculty, FacultyProgram, AdmissionStep, Stat, Testimonial,
    Partner, License, HomeFAQ, FinalCTA,
)


async def upsert_hero(session):
    existing = (await session.execute(
        select(HeroSettings).where(HeroSettings.page == "home")
    )).scalar_one_or_none()
    if existing:
        print("  hero already exists, skipping")
        return
    session.add(HeroSettings(
        page="home",
        variant="split",
        enabled=True,

        eyebrow_uz="O'zbekistonning yetakchi xususiy universiteti",
        eyebrow_ru="Ведущий частный университет Узбекистана",
        eyebrow_en="Uzbekistan's leading private university",

        title_uz="Bilim,",
        title_ru="Знание,",
        title_en="Knowledge,",
        title_highlight_uz="innovatsiya",
        title_highlight_ru="инновации",
        title_highlight_en="innovation",
        title_tail_uz="va kelajak.",
        title_tail_ru="и будущее.",
        title_tail_en="and the future.",

        subtitle_uz="Xalqaro standartlarda ta'lim, jahon darajasida professorlar va zamonaviy infratuzilma — XIU Edu sizning kelajagingiz uchun yagona manzil.",
        subtitle_ru="Международные стандарты образования, профессора мирового уровня и современная инфраструктура — XIU Edu единый адрес для вашего будущего.",
        subtitle_en="World-class faculty, international standards and modern infrastructure — XIU Edu is the single address for your future.",

        side_image="https://picsum.photos/seed/xiu-hero-photo/720/900",
        bg_image=None,
        bg_video=None,
        bg_video_poster=None,
        overlay_opacity=55,

        cta_primary_label_uz="Hujjat topshirish",
        cta_primary_label_ru="Подать документы",
        cta_primary_label_en="Apply now",
        cta_primary_url="https://admission.xiuedu.uz",
        cta_primary_external=True,

        cta_secondary_label_uz="Video tur",
        cta_secondary_label_ru="Видеотур",
        cta_secondary_label_en="Watch tour",
        cta_secondary_url="/about",
        cta_secondary_external=False,

        show_particles=True,
        show_scroll_indicator=True,
        show_trust_badges=True,
        show_floating_cards=True,

        quote_text_uz="Bu yerda men nafaqat bilim, balki kelajakka aniq qadam tashlash imkoniyatini topdim.",
        quote_text_ru="Здесь я нашла не только знания, но и возможность сделать конкретный шаг в будущее.",
        quote_text_en="Here I found not just knowledge but a clear path into my future.",
        quote_author_uz="Madina K. — Bitiruvchi 2024",
        quote_author_ru="Мадина К. — Выпускница 2024",
        quote_author_en="Madina K. — Graduate 2024",
    ))
    print("  hero seeded")


SECTIONS = [
    "intro", "news", "campus", "why_xiu", "academic", "admission",
    "numbers", "events", "testimonials", "partners", "licenses", "faq",
]
async def upsert_sections(session):
    for i, key in enumerate(SECTIONS):
        existing = (await session.execute(
            select(HomeSection).where(HomeSection.key == key)
        )).scalar_one_or_none()
        if existing:
            continue
        session.add(HomeSection(key=key, enabled=True, sort_order=i, settings={}))
    print(f"  {len(SECTIONS)} sections seeded")


QUICK_ACTIONS = [
    dict(icon="ArrowUpRightIcon", title_uz="Onlayn ariza",  title_ru="Онлайн заявка",   title_en="Online application",
         desc_uz="5 daqiqada hujjat topshiring",            desc_ru="Подайте документы за 5 минут", desc_en="Apply in 5 minutes",
         url="https://admission.xiuedu.uz", external=True, accent=True),
    dict(icon="BookOpenIcon",     title_uz="Yo'nalishlar",   title_ru="Направления",      title_en="Programs",
         desc_uz="Bakalavr va magistratura",                desc_ru="Бакалавриат и магистратура",     desc_en="Bachelor's and Master's",
         url="/faculties", external=False, accent=False),
    dict(icon="UserCircleIcon",   title_uz="HEMIS tizimi",   title_ru="HEMIS",             title_en="HEMIS",
         desc_uz="Talabalar uchun portal",                  desc_ru="Портал для студентов",           desc_en="Student portal",
         url="https://student.xiuedu.uz", external=True, accent=False),
    dict(icon="CalendarDaysIcon", title_uz="O'quv kalendari", title_ru="Учебный календарь", title_en="Academic calendar",
         desc_uz="Sana va tadbirlar",                       desc_ru="Даты и события",                 desc_en="Dates and events",
         url="/events", external=False, accent=False),
]
async def seed_quick_actions(session):
    if (await session.execute(select(QuickAction))).first():
        print("  quick actions already exist")
        return
    for i, qa in enumerate(QUICK_ACTIONS):
        session.add(QuickAction(sort_order=i, enabled=True, **qa))
    print(f"  {len(QUICK_ACTIONS)} quick actions seeded")


INTRO_PILLARS = [
    dict(icon="ShieldCheckIcon",
         title_uz="Akkreditatsiyalangan ta'lim", title_ru="Аккредитованное образование", title_en="Accredited education",
         desc_uz="Davlat va xalqaro standartlar bo'yicha tasdiqlangan dasturlar.",
         desc_ru="Программы, утверждённые государственными и международными стандартами.",
         desc_en="Programs approved by national and international standards."),
    dict(icon="GlobeAltIcon",
         title_uz="Xalqaro yo'nalish", title_ru="Международная направленность", title_en="Global outlook",
         desc_uz="Bolonya jarayoni, ECTS kreditlar va 50+ partner universitet.",
         desc_ru="Болонский процесс, ECTS-кредиты и 50+ университетов-партнёров.",
         desc_en="Bologna process, ECTS credits and 50+ partner universities."),
    dict(icon="SparklesIcon",
         title_uz="Innovatsion yondashuv", title_ru="Инновационный подход", title_en="Innovative approach",
         desc_uz="Zamonaviy laboratoriya, raqamli platformalar va loyiha asosida o'qitish.",
         desc_ru="Современные лаборатории, цифровые платформы и проектное обучение.",
         desc_en="Modern labs, digital platforms and project-based learning."),
]
async def seed_intro_pillars(session):
    if (await session.execute(select(IntroPillar))).first():
        return
    for i, p in enumerate(INTRO_PILLARS):
        session.add(IntroPillar(sort_order=i, enabled=True, **p))
    print(f"  {len(INTRO_PILLARS)} intro pillars seeded")


async def seed_campus(session):
    if (await session.execute(select(CampusSection))).first():
        return
    session.add(CampusSection(
        main_image="https://picsum.photos/seed/xiu-campus-main/800/800",
        image_2="https://picsum.photos/seed/xiu-campus-2/400/400",
        image_3="https://picsum.photos/seed/xiu-campus-3/400/400",
        eyebrow_uz="Talabalar hayoti",            eyebrow_ru="Студенческая жизнь",   eyebrow_en="Student life",
        title_uz="Bizning kampus",                title_ru="Наш кампус",             title_en="Our campus",
        text_uz="Zamonaviy auditoriya, kutubxona, sport zali va talabalar klublari — siz uchun ikkinchi uy.",
        text_ru="Современные аудитории, библиотека, спортзал и студенческие клубы — ваш второй дом.",
        text_en="Modern classrooms, library, sports hall and student clubs — your second home.",
        bullets=[
            {"uz": "Zamonaviy auditoriya va IT laboratoriyalar",
             "ru": "Современные аудитории и IT-лаборатории",
             "en": "Modern classrooms and IT labs"},
            {"uz": "Til markazi va ko'p tilli kutubxona",
             "ru": "Языковой центр и многоязычная библиотека",
             "en": "Language centre and multilingual library"},
            {"uz": "Sport zali, kafe va talabalar klublari",
             "ru": "Спортзал, кафе и студенческие клубы",
             "en": "Sports hall, café and student clubs"},
        ],
        cta_label_uz="Galereyani ko'rish", cta_label_ru="Посмотреть галерею", cta_label_en="View gallery",
        cta_url="/gallery",
    ))
    print("  campus section seeded")


WHY_CARDS = [
    dict(icon="GlobeAltIcon",        icon_bg="bg-primary-50",  icon_color="text-primary-700",
         number="50+",  number_label_uz="partner",   number_label_ru="партнёр",  number_label_en="partners",
         title_uz="Xalqaro standartlar",      title_ru="Международные стандарты",  title_en="International standards",
         desc_uz="Bolonya jarayoni, ECTS kredit tizimi va Cambridge English bilan rasmiy hamkorlik.",
         desc_ru="Болонский процесс, ECTS и официальное партнёрство с Cambridge English.",
         desc_en="Bologna process, ECTS credit system and official Cambridge English partnership."),
    dict(icon="UserGroupIcon",       icon_bg="bg-accent-50",   icon_color="text-accent-600",
         number="150+", number_label_uz="professor", number_label_ru="профессор", number_label_en="professors",
         title_uz="Tajribali professorlar",   title_ru="Опытные преподаватели",     title_en="Experienced faculty",
         desc_uz="150+ professor-o'qituvchi, ulardan 60% xorijiy universitetlarda tajriba olgan.",
         desc_ru="150+ преподавателей, 60% из которых имеют опыт работы в зарубежных университетах.",
         desc_en="150+ professors, 60% with experience at foreign universities."),
    dict(icon="BriefcaseIcon",       icon_bg="bg-emerald-50",  icon_color="text-emerald-700",
         number="95%",  number_label_uz="ish bilan", number_label_ru="трудоустроено", number_label_en="employed",
         title_uz="Karyera istiqboli",         title_ru="Карьерные перспективы",     title_en="Career outcomes",
         desc_uz="Bitiruvchilarimizning 95% bitirganidan keyin 6 oy ichida ishga joylashgan.",
         desc_ru="95% наших выпускников трудоустраиваются в течение 6 месяцев.",
         desc_en="95% of our graduates are employed within 6 months of graduation."),
    dict(icon="BuildingOffice2Icon", icon_bg="bg-purple-50",   icon_color="text-purple-700",
         number="12",   number_label_uz="yo'nalish", number_label_ru="направлений", number_label_en="programs",
         title_uz="Zamonaviy kampus",          title_ru="Современный кампус",        title_en="Modern campus",
         desc_uz="IT laboratoriyasi, til markazi, kutubxona va talabalar yashash binolari.",
         desc_ru="IT-лаборатории, языковой центр, библиотека и студенческое общежитие.",
         desc_en="IT labs, language centre, library and student dormitories."),
]
async def seed_why_cards(session):
    if (await session.execute(select(WhyCard))).first():
        return
    for i, c in enumerate(WHY_CARDS):
        session.add(WhyCard(sort_order=i, enabled=True, **c))
    print(f"  {len(WHY_CARDS)} why cards seeded")


# ── Faculties + Programs ──
FACULTIES = [
    dict(slug="pedagogika", icon="AcademicCapIcon",
         name_uz="Pedagogika", name_ru="Педагогика", name_en="Pedagogy",
         description_uz="Ta'lim, psixologiya va metodika yo'nalishlari",
         description_ru="Образование, психология и методические направления",
         description_en="Education, psychology and methodology programs",
         programs=[
             dict(icon="BookOpenIcon",
                  name_uz="Boshlang'ich ta'lim", name_ru="Начальное образование", name_en="Primary education",
                  bg_class="bg-indigo-50  dark:bg-indigo-900/15",  icon_bg_class="bg-indigo-500",  ring_class="ring-indigo-200/60",
                  duration_uz="4 yil", duration_ru="4 года", duration_en="4 years",
                  tuition="16 mln", language_uz="O'zbek", language_ru="Узбекский", language_en="Uzbek"),
             dict(icon="UserGroupIcon",
                  name_uz="Maktabgacha ta'lim", name_ru="Дошкольное образование", name_en="Preschool education",
                  bg_class="bg-blue-50    dark:bg-blue-900/15",    icon_bg_class="bg-blue-500",    ring_class="ring-blue-200/60",
                  duration_uz="4 yil", duration_ru="4 года", duration_en="4 years",
                  tuition="14 mln", language_uz="O'zbek", language_ru="Узбекский", language_en="Uzbek"),
             dict(icon="ChatBubbleLeftRightIcon",
                  name_uz="Pedagogika va psixologiya", name_ru="Педагогика и психология", name_en="Pedagogy and psychology",
                  bg_class="bg-violet-50  dark:bg-violet-900/15",  icon_bg_class="bg-violet-500",  ring_class="ring-violet-200/60",
                  duration_uz="2 yil (M)", duration_ru="2 года (М)", duration_en="2 years (M)",
                  tuition="22 mln", language_uz="O'zbek", language_ru="Узбекский", language_en="Uzbek"),
             dict(icon="LightBulbIcon",
                  name_uz="Maxsus pedagogika", name_ru="Специальная педагогика", name_en="Special pedagogy",
                  bg_class="bg-fuchsia-50 dark:bg-fuchsia-900/15", icon_bg_class="bg-fuchsia-500", ring_class="ring-fuchsia-200/60",
                  duration_uz="4 yil", duration_ru="4 года", duration_en="4 years",
                  tuition="15 mln", language_uz="O'zbek", language_ru="Узбекский", language_en="Uzbek"),
         ]),
    dict(slug="iqtisodiyot", icon="ChartBarIcon",
         name_uz="Iqtisodiyot", name_ru="Экономика", name_en="Economics",
         description_uz="Biznes, menejment, moliya va MBA dasturlari",
         description_ru="Бизнес, менеджмент, финансы и MBA",
         description_en="Business, management, finance and MBA",
         programs=[
             dict(icon="ChartBarIcon",
                  name_uz="Iqtisodiyot va menejment", name_ru="Экономика и менеджмент", name_en="Economics and management",
                  bg_class="bg-emerald-50 dark:bg-emerald-900/15", icon_bg_class="bg-emerald-500", ring_class="ring-emerald-200/60",
                  duration_uz="4 yil", duration_ru="4 года", duration_en="4 years",
                  tuition="18 mln", language_uz="O'zbek", language_ru="Узбекский", language_en="Uzbek"),
             dict(icon="MegaphoneIcon",
                  name_uz="Marketing", name_ru="Маркетинг", name_en="Marketing",
                  bg_class="bg-rose-50    dark:bg-rose-900/15",    icon_bg_class="bg-rose-500",    ring_class="ring-rose-200/60",
                  duration_uz="4 yil", duration_ru="4 года", duration_en="4 years",
                  tuition="18 mln", language_uz="Ingliz", language_ru="Английский", language_en="English"),
             dict(icon="BanknotesIcon",
                  name_uz="Moliya va bank ishi", name_ru="Финансы и банковское дело", name_en="Finance and banking",
                  bg_class="bg-teal-50    dark:bg-teal-900/15",    icon_bg_class="bg-teal-500",    ring_class="ring-teal-200/60",
                  duration_uz="4 yil", duration_ru="4 года", duration_en="4 years",
                  tuition="19 mln", language_uz="O'zbek", language_ru="Узбекский", language_en="Uzbek"),
             dict(icon="BriefcaseIcon",
                  name_uz="MBA", name_ru="MBA", name_en="MBA",
                  bg_class="bg-amber-50   dark:bg-amber-900/15",   icon_bg_class="bg-amber-500",   ring_class="ring-amber-200/60",
                  duration_uz="1.5 yil", duration_ru="1.5 года", duration_en="1.5 years",
                  tuition="32 mln", language_uz="Ingliz", language_ru="Английский", language_en="English"),
         ]),
    dict(slug="filologiya", icon="LanguageIcon",
         name_uz="Filologiya", name_ru="Филология", name_en="Philology",
         description_uz="Tillar, adabiyot va tarjimashunoslik",
         description_ru="Языки, литература и переводоведение",
         description_en="Languages, literature and translation",
         programs=[
             dict(icon="LanguageIcon",
                  name_uz="Ingliz tili va adabiyoti", name_ru="Английский язык и литература", name_en="English language and literature",
                  bg_class="bg-amber-50  dark:bg-amber-900/15",  icon_bg_class="bg-amber-500",   ring_class="ring-amber-200/60",
                  duration_uz="4 yil", duration_ru="4 года", duration_en="4 years",
                  tuition="17 mln", language_uz="Ingliz", language_ru="Английский", language_en="English"),
             dict(icon="GlobeAltIcon",
                  name_uz="Tarjimashunoslik", name_ru="Переводоведение", name_en="Translation studies",
                  bg_class="bg-orange-50 dark:bg-orange-900/15", icon_bg_class="bg-orange-500",  ring_class="ring-orange-200/60",
                  duration_uz="4 yil", duration_ru="4 года", duration_en="4 years",
                  tuition="17 mln", language_uz="Ingliz", language_ru="Английский", language_en="English"),
             dict(icon="BookOpenIcon",
                  name_uz="Lingvistika", name_ru="Лингвистика", name_en="Linguistics",
                  bg_class="bg-yellow-50 dark:bg-yellow-900/15", icon_bg_class="bg-yellow-500",  ring_class="ring-yellow-200/60",
                  duration_uz="2 yil (M)", duration_ru="2 года (М)", duration_en="2 years (M)",
                  tuition="21 mln", language_uz="Ingliz", language_ru="Английский", language_en="English"),
             dict(icon="PencilSquareIcon",
                  name_uz="Akademik yozish", name_ru="Академическое письмо", name_en="Academic writing",
                  bg_class="bg-red-50    dark:bg-red-900/15",    icon_bg_class="bg-red-500",     ring_class="ring-red-200/60",
                  duration_uz="3 oy", duration_ru="3 месяца", duration_en="3 months",
                  tuition="2.5 mln", language_uz="Ingliz", language_ru="Английский", language_en="English"),
         ]),
    dict(slug="huquq", icon="ScaleIcon",
         name_uz="Huquqshunoslik", name_ru="Юриспруденция", name_en="Law",
         description_uz="Yuridik fanlar va xalqaro huquq",
         description_ru="Юридические науки и международное право",
         description_en="Legal studies and international law",
         programs=[
             dict(icon="GlobeAltIcon",
                  name_uz="Xalqaro huquq", name_ru="Международное право", name_en="International law",
                  bg_class="bg-slate-50  dark:bg-slate-800/40",  icon_bg_class="bg-slate-700",   ring_class="ring-slate-200/60",
                  duration_uz="4 yil", duration_ru="4 года", duration_en="4 years",
                  tuition="18 mln", language_uz="O'zbek/Ingliz", language_ru="Узбекский/Английский", language_en="Uzbek/English"),
             dict(icon="ScaleIcon",
                  name_uz="Fuqarolik huquqi", name_ru="Гражданское право", name_en="Civil law",
                  bg_class="bg-stone-50  dark:bg-stone-800/40",  icon_bg_class="bg-stone-700",   ring_class="ring-stone-200/60",
                  duration_uz="4 yil", duration_ru="4 года", duration_en="4 years",
                  tuition="17 mln", language_uz="O'zbek", language_ru="Узбекский", language_en="Uzbek"),
             dict(icon="ShieldCheckIcon",
                  name_uz="Jinoyat huquqi", name_ru="Уголовное право", name_en="Criminal law",
                  bg_class="bg-zinc-50   dark:bg-zinc-800/40",   icon_bg_class="bg-zinc-700",    ring_class="ring-zinc-200/60",
                  duration_uz="4 yil", duration_ru="4 года", duration_en="4 years",
                  tuition="17 mln", language_uz="O'zbek", language_ru="Узбекский", language_en="Uzbek"),
             dict(icon="BuildingOffice2Icon",
                  name_uz="Korporativ huquq", name_ru="Корпоративное право", name_en="Corporate law",
                  bg_class="bg-neutral-50 dark:bg-neutral-800/40", icon_bg_class="bg-neutral-700", ring_class="ring-neutral-200/60",
                  duration_uz="2 yil (M)", duration_ru="2 года (М)", duration_en="2 years (M)",
                  tuition="24 mln", language_uz="Ingliz", language_ru="Английский", language_en="English"),
         ]),
    dict(slug="it", icon="ComputerDesktopIcon",
         name_uz="IT va Muhandislik", name_ru="ИТ и инженерия", name_en="IT and Engineering",
         description_uz="Dasturlash, AI va ma'lumotlar fanlari",
         description_ru="Программирование, ИИ и науки о данных",
         description_en="Programming, AI and data science",
         programs=[
             dict(icon="CodeBracketIcon",
                  name_uz="Dasturiy injiniring", name_ru="Программная инженерия", name_en="Software engineering",
                  bg_class="bg-sky-50    dark:bg-sky-900/15",    icon_bg_class="bg-sky-500",    ring_class="ring-sky-200/60",
                  duration_uz="4 yil", duration_ru="4 года", duration_en="4 years",
                  tuition="22 mln", language_uz="Ingliz", language_ru="Английский", language_en="English"),
             dict(icon="ServerStackIcon",
                  name_uz="Ma'lumotlar fani", name_ru="Наука о данных", name_en="Data science",
                  bg_class="bg-cyan-50   dark:bg-cyan-900/15",   icon_bg_class="bg-cyan-500",   ring_class="ring-cyan-200/60",
                  duration_uz="4 yil", duration_ru="4 года", duration_en="4 years",
                  tuition="22 mln", language_uz="Ingliz", language_ru="Английский", language_en="English"),
             dict(icon="LockClosedIcon",
                  name_uz="Cyber xavfsizlik", name_ru="Кибербезопасность", name_en="Cyber security",
                  bg_class="bg-blue-50   dark:bg-blue-900/15",   icon_bg_class="bg-blue-600",   ring_class="ring-blue-200/60",
                  duration_uz="4 yil", duration_ru="4 года", duration_en="4 years",
                  tuition="24 mln", language_uz="Ingliz", language_ru="Английский", language_en="English"),
             dict(icon="CpuChipIcon",
                  name_uz="AI va Machine Learning", name_ru="ИИ и машинное обучение", name_en="AI and machine learning",
                  bg_class="bg-indigo-50 dark:bg-indigo-900/15", icon_bg_class="bg-indigo-600", ring_class="ring-indigo-200/60",
                  duration_uz="2 yil (M)", duration_ru="2 года (М)", duration_en="2 years (M)",
                  tuition="28 mln", language_uz="Ingliz", language_ru="Английский", language_en="English"),
         ]),
    dict(slug="sanat", icon="PaintBrushIcon",
         name_uz="Dizayn va san'at", name_ru="Дизайн и искусство", name_en="Design and Arts",
         description_uz="Grafik dizayn va vizual kommunikatsiya",
         description_ru="Графический дизайн и визуальные коммуникации",
         description_en="Graphic design and visual communication",
         programs=[
             dict(icon="PaintBrushIcon",
                  name_uz="Grafik dizayn", name_ru="Графический дизайн", name_en="Graphic design",
                  bg_class="bg-pink-50    dark:bg-pink-900/15",    icon_bg_class="bg-pink-500",    ring_class="ring-pink-200/60",
                  duration_uz="4 yil", duration_ru="4 года", duration_en="4 years",
                  tuition="16 mln", language_uz="O'zbek", language_ru="Узбекский", language_en="Uzbek"),
             dict(icon="ComputerDesktopIcon",
                  name_uz="UX/UI dizayn", name_ru="UX/UI дизайн", name_en="UX/UI design",
                  bg_class="bg-rose-50    dark:bg-rose-900/15",    icon_bg_class="bg-rose-500",    ring_class="ring-rose-200/60",
                  duration_uz="3 oy", duration_ru="3 месяца", duration_en="3 months",
                  tuition="3 mln", language_uz="Ingliz", language_ru="Английский", language_en="English"),
             dict(icon="CameraIcon",
                  name_uz="Fotografiya", name_ru="Фотография", name_en="Photography",
                  bg_class="bg-fuchsia-50 dark:bg-fuchsia-900/15", icon_bg_class="bg-fuchsia-500", ring_class="ring-fuchsia-200/60",
                  duration_uz="4 oy", duration_ru="4 месяца", duration_en="4 months",
                  tuition="3 mln", language_uz="O'zbek", language_ru="Узбекский", language_en="Uzbek"),
             dict(icon="SparklesIcon",
                  name_uz="San'atshunoslik", name_ru="Искусствоведение", name_en="Art studies",
                  bg_class="bg-purple-50  dark:bg-purple-900/15",  icon_bg_class="bg-purple-500",  ring_class="ring-purple-200/60",
                  duration_uz="4 yil", duration_ru="4 года", duration_en="4 years",
                  tuition="15 mln", language_uz="O'zbek", language_ru="Узбекский", language_en="Uzbek"),
         ]),
]
async def seed_faculties(session):
    if (await session.execute(select(Faculty))).first():
        print("  faculties already exist")
        return
    for i, f in enumerate(FACULTIES):
        programs = f.pop("programs")
        fac = Faculty(sort_order=i, enabled=True, **f)
        session.add(fac)
        await session.flush()
        for j, p in enumerate(programs):
            session.add(FacultyProgram(faculty_id=fac.id, sort_order=j, enabled=True, **p))
    print(f"  {len(FACULTIES)} faculties + programs seeded")


ADMISSION_STEPS = [
    dict(number="01", icon="DocumentTextIcon",
         title_uz="Ariza topshirish", title_ru="Подача заявки", title_en="Submit application",
         desc_uz="Onlayn formada shaxsiy ma'lumotlarni kiriting va yo'nalishni tanlang.",
         desc_ru="Заполните онлайн-форму с личными данными и выберите направление.",
         desc_en="Fill out the online form with your details and choose a program."),
    dict(number="02", icon="ClipboardDocumentCheckIcon",
         title_uz="Hujjatlar tekshiruvi", title_ru="Проверка документов", title_en="Document review",
         desc_uz="Qabul komissiyasi hujjatlaringizni 1-3 ish kuni ichida ko'rib chiqadi.",
         desc_ru="Приёмная комиссия рассмотрит документы за 1–3 рабочих дня.",
         desc_en="The admissions committee reviews your documents within 1–3 working days."),
    dict(number="03", icon="IdentificationIcon",
         title_uz="Suhbat / imtihon", title_ru="Собеседование / экзамен", title_en="Interview / exam",
         desc_uz="Qisqa motivatsion suhbat yoki tegishli kirish imtihoni topshirasiz.",
         desc_ru="Краткое мотивационное собеседование или вступительный экзамен.",
         desc_en="A short motivational interview or relevant entrance examination."),
    dict(number="04", icon="SparklesIcon",
         title_uz="Qabul va ro'yxat", title_ru="Зачисление", title_en="Enrollment",
         desc_uz="Tabriklaymiz! Shartnomani imzolang va o'quv yiliga tayyorlaning.",
         desc_ru="Поздравляем! Подпишите договор и готовьтесь к учёбе.",
         desc_en="Congratulations! Sign the contract and prepare for the academic year."),
]
async def seed_admission_steps(session):
    if (await session.execute(select(AdmissionStep))).first():
        return
    for i, s in enumerate(ADMISSION_STEPS):
        session.add(AdmissionStep(sort_order=i, enabled=True, **s))
    print(f"  {len(ADMISSION_STEPS)} admission steps seeded")


STATS = [
    dict(value="5,000+",  label_uz="Hozirgi talabalar", label_ru="Текущие студенты",  label_en="Current students",
         sub_uz="Barcha yo'nalishlar", sub_ru="Все направления", sub_en="All programs"),
    dict(value="12,000+", label_uz="Bitiruvchilarimiz", label_ru="Наших выпускников", label_en="Our graduates",
         sub_uz="2009 yildan beri", sub_ru="С 2009 года", sub_en="Since 2009"),
    dict(value="95%",     label_uz="Ish bilan ta'minlanganlik", label_ru="Трудоустройство", label_en="Employment rate",
         sub_uz="6 oy ichida", sub_ru="В течение 6 месяцев", sub_en="Within 6 months"),
    dict(value="50+",     label_uz="Xalqaro hamkor", label_ru="Международных партнёров", label_en="International partners",
         sub_uz="15 mamlakatda", sub_ru="В 15 странах", sub_en="Across 15 countries"),
]
async def seed_stats(session):
    if (await session.execute(select(Stat))).first():
        return
    for i, s in enumerate(STATS):
        session.add(Stat(sort_order=i, enabled=True, **s))
    print(f"  {len(STATS)} stats seeded")


TESTIMONIALS = [
    dict(name_uz="Madina Karimova",  name_ru="Мадина Каримова",  name_en="Madina Karimova",
         role_uz="Filologiya, 2024", role_ru="Филология, 2024", role_en="Philology, 2024",
         text_uz="XIU da o'qigan to'rt yilim hayotimning eng yaxshi davri bo'ldi. Cambridge English dasturi tufayli IELTS-da 8.0 ball oldim va hozir London Business School magistraturasini o'qiyapman.",
         text_ru="Четыре года в XIU стали лучшим временем моей жизни. Благодаря программе Cambridge English я получила 8.0 в IELTS и сейчас учусь в магистратуре London Business School.",
         text_en="My four years at XIU were the best time of my life. Thanks to the Cambridge English program I scored 8.0 in IELTS and now study at London Business School.",
         avatar="https://i.pravatar.cc/120?img=44", year=2024),
    dict(name_uz="Bekzod Tursunov",  name_ru="Бекзод Турсунов",  name_en="Bekzod Tursunov",
         role_uz="MBA, 2023", role_ru="MBA, 2023", role_en="MBA, 2023",
         text_uz="Iqtisodiyot fakulteti meni real biznes sharoitiga tayyorladi. MBA dasturidan keyin o'z startupimni ochdim va birinchi yil ichida 200 ming dollar daromad oldim.",
         text_ru="Экономический факультет подготовил меня к реальному бизнесу. После MBA я открыл свой стартап и заработал $200K в первый год.",
         text_en="The economics faculty prepared me for real business. After the MBA I launched my own startup and earned $200K in the first year.",
         avatar="https://i.pravatar.cc/120?img=33", year=2023),
    dict(name_uz="Nodira Yusupova", name_ru="Нодира Юсупова",  name_en="Nodira Yusupova",
         role_uz="Pedagogika, 2022", role_ru="Педагогика, 2022", role_en="Pedagogy, 2022",
         text_uz="Pedagogika fakultetida zamonaviy metodikani o'rgandim. Hozir o'z xususiy maktabimni boshqaraman va 300 dan ortiq bolaga ta'lim beraman.",
         text_ru="На педагогическом факультете я изучила современные методики. Сейчас управляю своей частной школой и обучаю более 300 детей.",
         text_en="At the pedagogy faculty I learned modern teaching methods. Now I run my own private school and teach more than 300 children.",
         avatar="https://i.pravatar.cc/120?img=49", year=2022),
]
async def seed_testimonials(session):
    if (await session.execute(select(Testimonial))).first():
        return
    for i, t in enumerate(TESTIMONIALS):
        session.add(Testimonial(sort_order=i, enabled=True, **t))
    print(f"  {len(TESTIMONIALS)} testimonials seeded")


PARTNERS = [
    ("🇬🇧", "Buyuk Britaniya", "Великобритания",   "United Kingdom", 8),
    ("🇺🇸", "AQSH",            "США",               "USA",            6),
    ("🇩🇪", "Germaniya",       "Германия",          "Germany",        5),
    ("🇰🇷", "Janubiy Koreya",  "Южная Корея",       "South Korea",    4),
    ("🇯🇵", "Yaponiya",        "Япония",            "Japan",          3),
    ("🇹🇷", "Turkiya",         "Турция",            "Turkey",         7),
    ("🇨🇿", "Chexiya",         "Чехия",             "Czech Republic", 3),
    ("🇲🇾", "Malayziya",       "Малайзия",          "Malaysia",       4),
    ("🇮🇳", "Hindiston",       "Индия",             "India",          5),
    ("🇨🇳", "Xitoy",           "Китай",             "China",          5),
]
async def seed_partners(session):
    if (await session.execute(select(Partner))).first():
        return
    for i, (flag, uz, ru, en, count) in enumerate(PARTNERS):
        session.add(Partner(sort_order=i, enabled=True, flag=flag,
                            country_uz=uz, country_ru=ru, country_en=en, count=count))
    print(f"  {len(PARTNERS)} partners seeded")


LICENSES = [
    dict(title_uz="Oliy ta'lim vazirligi litsenziyasi", title_ru="Лицензия Министерства высшего образования", title_en="Ministry of Higher Education licence",
         issuer_uz="O'zbekiston Respublikasi OTV", issuer_ru="Министерство Республики Узбекистан", issuer_en="Republic of Uzbekistan MoHE",
         year=2024, image="https://picsum.photos/seed/xiu-license-1/600/848"),
    dict(title_uz="ISO 9001:2015 sertifikati", title_ru="Сертификат ISO 9001:2015", title_en="ISO 9001:2015 certificate",
         issuer_uz="TÜV International", issuer_ru="TÜV International", issuer_en="TÜV International",
         year=2024, image="https://picsum.photos/seed/xiu-license-2/600/848"),
    dict(title_uz="Cambridge English Partner", title_ru="Cambridge English Partner", title_en="Cambridge English Partner",
         issuer_uz="Cambridge Assessment", issuer_ru="Cambridge Assessment", issuer_en="Cambridge Assessment",
         year=2023, image="https://picsum.photos/seed/xiu-license-3/600/848"),
    dict(title_uz="Davlat akkreditatsiyasi", title_ru="Государственная аккредитация", title_en="State accreditation",
         issuer_uz="Ta'lim sifatini nazorat qilish davlat inspektsiyasi",
         issuer_ru="Государственная инспекция по контролю качества образования",
         issuer_en="State Inspection for Quality Control of Education",
         year=2023, image="https://picsum.photos/seed/xiu-license-4/600/848"),
]
async def seed_licenses(session):
    if (await session.execute(select(License))).first():
        return
    for i, l in enumerate(LICENSES):
        session.add(License(sort_order=i, enabled=True, **l))
    print(f"  {len(LICENSES)} licenses seeded")


FAQS = [
    dict(question_uz="Qabul muddati qachon?", question_ru="Когда сроки приёма?", question_en="When is the admission period?",
         answer_uz="Asosiy qabul iyun-iyul oylarida o'tkaziladi. Onlayn ariza yil davomida ochiq.",
         answer_ru="Основной приём проходит в июне–июле. Онлайн-заявка открыта круглый год.",
         answer_en="The main admission runs in June–July. Online application is open year-round."),
    dict(question_uz="Stipendiya berishadimi?", question_ru="Есть ли стипендии?", question_en="Are there scholarships?",
         answer_uz="Ha, eng yaxshi natijalar uchun grant va stipendiya tizimi mavjud. Imtihon natijalari va akademik ko'rsatkichlarga qarab beriladi.",
         answer_ru="Да, для лучших абитуриентов предусмотрены гранты и стипендии по результатам экзаменов и академическим показателям.",
         answer_en="Yes, grants and scholarships are awarded for top performers based on exams and academic results."),
    dict(question_uz="Chet ellik talabalar qabul qilinadimi?", question_ru="Принимаете ли иностранных студентов?", question_en="Do you accept international students?",
         answer_uz="Albatta. Xalqaro talabalar uchun maxsus dasturlar va yotoqxona xizmati mavjud.",
         answer_ru="Конечно. Для иностранных студентов есть специальные программы и общежитие.",
         answer_en="Absolutely. There are dedicated programs and dormitory services for international students."),
    dict(question_uz="O'qish narxi qancha?", question_ru="Сколько стоит обучение?", question_en="How much is tuition?",
         answer_uz="Bakalavr 14-18 mln so'm/yil, magistratura 21-32 mln so'm/yil oraligida. Bo'lib to'lash imkoniyati bor.",
         answer_ru="Бакалавриат 14–18 млн сум/год, магистратура 21–32 млн сум/год. Возможна оплата частями.",
         answer_en="Bachelor's 14–18M UZS/year, Master's 21–32M UZS/year. Installment payments are available."),
    dict(question_uz="Yotoqxona berishadimi?", question_ru="Предоставляете общежитие?", question_en="Do you offer dormitory?",
         answer_uz="Boshqa shahardan kelgan talabalar uchun zamonaviy yotoqxona xonalari ajratiladi.",
         answer_ru="Да, для иногородних студентов выделяются современные комнаты.",
         answer_en="Yes, modern rooms are allocated for students from other regions."),
]
async def seed_faqs(session):
    if (await session.execute(select(HomeFAQ))).first():
        return
    for i, q in enumerate(FAQS):
        session.add(HomeFAQ(sort_order=i, enabled=True, **q))
    print(f"  {len(FAQS)} FAQs seeded")


async def seed_final_cta(session):
    if (await session.execute(select(FinalCTA))).first():
        return
    session.add(FinalCTA(
        enabled=True,
        eyebrow_uz="2026 / 2027 qabul",       eyebrow_ru="Приём 2026 / 2027",       eyebrow_en="2026 / 2027 admissions",
        title_uz="Kelajagingizni hozirdan boshlang",
        title_ru="Начните своё будущее уже сегодня",
        title_en="Start your future today",
        text_uz="Hujjat qabuli iyun oyidan boshlanadi. Joylar cheklangan — hozirdan ariza topshiring.",
        text_ru="Приём документов открывается в июне. Места ограничены — подайте заявку сейчас.",
        text_en="Document intake opens in June. Seats are limited — apply now.",
        cta_label_uz="Onlayn ariza topshirish", cta_label_ru="Подать онлайн-заявку", cta_label_en="Apply online",
        cta_url="https://admission.xiuedu.uz", cta_external=True,
        phone_label="+998 55 406-15-15", phone_url="+998554061515",
    ))
    print("  final CTA seeded")


async def main():
    async with AsyncSessionLocal() as session:
        print("=== Seeding home page CMS ===")
        await upsert_hero(session)
        await upsert_sections(session)
        await seed_quick_actions(session)
        await seed_intro_pillars(session)
        await seed_campus(session)
        await seed_why_cards(session)
        await seed_faculties(session)
        await seed_admission_steps(session)
        await seed_stats(session)
        await seed_testimonials(session)
        await seed_partners(session)
        await seed_licenses(session)
        await seed_faqs(session)
        await seed_final_cta(session)
        await session.commit()
        print("=== Done ===")


if __name__ == "__main__":
    asyncio.run(main())
