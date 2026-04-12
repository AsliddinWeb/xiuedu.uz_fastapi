"""
Seed Applicants page CMS with the values previously hardcoded.
"""
import asyncio, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models.applicants_page import (
    ApplicantsPage, ApplicantsStep, ApplicantsForm,
    ApplicantsTimelineItem, ApplicantsDocCategory, ApplicantsFaq,
)


async def upsert_page(session):
    if (await session.execute(select(ApplicantsPage).limit(1))).scalar_one_or_none():
        print("  ApplicantsPage already seeded"); return
    session.add(ApplicantsPage(
        # Section eyebrows + titles
        steps_eyebrow_uz="Qabul jarayoni", steps_eyebrow_ru="Процесс приёма", steps_eyebrow_en="Admission process",
        steps_title_uz="4 oddiy qadam", steps_title_ru="4 простых шага", steps_title_en="4 simple steps",

        forms_eyebrow_uz="Ta'lim shakllari", forms_eyebrow_ru="Формы обучения", forms_eyebrow_en="Study modes",
        forms_title_uz="O'zingizga mos shaklni tanlang",
        forms_title_ru="Выберите подходящую форму",
        forms_title_en="Choose the right format for you",

        timeline_eyebrow_uz="Qabul muddatlari", timeline_eyebrow_ru="Сроки приёма", timeline_eyebrow_en="Admission dates",
        timeline_title_uz="Asosiy sanalar", timeline_title_ru="Ключевые даты", timeline_title_en="Key dates",

        docs_eyebrow_uz="Hujjatlar", docs_eyebrow_ru="Документы", docs_eyebrow_en="Documents",
        docs_title_uz="Kerakli hujjatlar", docs_title_ru="Необходимые документы", docs_title_en="Required documents",

        faq_eyebrow_uz="FAQ", faq_eyebrow_ru="FAQ", faq_eyebrow_en="FAQ",
        faq_title_uz="Tez-tez beriladigan savollar",
        faq_title_ru="Часто задаваемые вопросы",
        faq_title_en="Frequently asked questions",

        # CTA
        cta_title_uz="Hozir ariza topshiring",
        cta_title_ru="Подайте заявку прямо сейчас",
        cta_title_en="Apply now",
        cta_text_uz="2026 / 2027 o'quv yiliga onlayn ariza topshirish ochiq. Joylar cheklangan.",
        cta_text_ru="Приём заявок на 2026 / 2027 учебный год открыт. Места ограничены.",
        cta_text_en="Applications for 2026/2027 are open. Seats are limited.",
        cta_primary_label_uz="Onlayn ariza topshirish",
        cta_primary_label_ru="Подать онлайн-заявку",
        cta_primary_label_en="Apply online",
        cta_primary_url="https://admission.xiuedu.uz",
        cta_primary_external=True,
        cta_phone_label="+998 55 406-15-15",
        cta_phone_url="+998554061515",
    ))
    print("  ApplicantsPage seeded")


STEPS = [
    dict(number=1, icon="DocumentTextIcon",
         title_uz="Hujjat tayyorlash", title_ru="Подготовка документов", title_en="Prepare documents",
         desc_uz="Pasport, attestat va boshqa hujjatlarni tayyorlang.",
         desc_ru="Подготовьте паспорт, аттестат и другие документы.",
         desc_en="Prepare passport, certificate and other documents."),
    dict(number=2, icon="ClipboardDocumentCheckIcon",
         title_uz="Ariza topshirish", title_ru="Подача заявки", title_en="Submit application",
         desc_uz="Onlayn ariza yoki qabul markazi orqali.",
         desc_ru="Через онлайн-форму или приёмный пункт.",
         desc_en="Via the online form or our admissions office."),
    dict(number=3, icon="IdentificationIcon",
         title_uz="Test va suhbat", title_ru="Тест и собеседование", title_en="Test and interview",
         desc_uz="Tanlangan yo'nalishga ko'ra imtihon yoki suhbat.",
         desc_ru="Экзамен или собеседование по выбранному направлению.",
         desc_en="Exam or interview based on the chosen program."),
    dict(number=4, icon="SparklesIcon",
         title_uz="Qabul", title_ru="Зачисление", title_en="Enrollment",
         desc_uz="Natijalar va kontrakt rasmiylashtirish.",
         desc_ru="Результаты и оформление договора.",
         desc_en="Results and contract signing."),
]


FORMS = [
    dict(title_uz="Kunduzgi ta'lim", title_ru="Очное обучение", title_en="Full-time",
         desc_uz="4 yil, haftalik 5 kun mashg'ulot, to'liq talabalik hayoti.",
         desc_ru="4 года, 5 дней в неделю, полноценная студенческая жизнь.",
         desc_en="4 years, 5 days a week, full student life.",
         features=[
             {"uz":"4 yil","ru":"4 года","en":"4 years"},
             {"uz":"Haftalik 5 kun","ru":"5 дней в неделю","en":"5 days a week"},
             {"uz":"Stipendiya","ru":"Стипендия","en":"Scholarships"}
         ],
         cta_label_uz="Batafsil", cta_label_ru="Подробнее", cta_label_en="Learn more",
         cta_url="/education/bachelor"),
    dict(title_uz="Sirtqi ta'lim", title_ru="Заочное обучение", title_en="Part-time",
         desc_uz="Ishlab o'qishni xohlovchilar uchun, sessiya tizimi.",
         desc_ru="Для тех, кто работает и учится, сессионная система.",
         desc_en="For those who work and study — session-based.",
         features=[
             {"uz":"4–5 yil","ru":"4–5 лет","en":"4–5 years"},
             {"uz":"Sessiya","ru":"Сессии","en":"Exam sessions"},
             {"uz":"Onlayn materiallar","ru":"Онлайн-материалы","en":"Online materials"}
         ],
         cta_label_uz="Batafsil", cta_label_ru="Подробнее", cta_label_en="Learn more",
         cta_url="/education/master"),
]


TIMELINE = [
    dict(month_uz="Iyun",    month_ru="Июнь",     month_en="June",
         text_uz="Onlayn ariza qabuli boshlanadi",
         text_ru="Открывается приём онлайн-заявок",
         text_en="Online application opens"),
    dict(month_uz="Iyul",    month_ru="Июль",     month_en="July",
         text_uz="Hujjat topshirish va imtihonlar",
         text_ru="Подача документов и экзамены",
         text_en="Document submission and exams"),
    dict(month_uz="Avgust",  month_ru="Август",   month_en="August",
         text_uz="Natijalar va qabul",
         text_ru="Результаты и зачисление",
         text_en="Results and enrollment"),
    dict(month_uz="Sentabr", month_ru="Сентябрь", month_en="September",
         text_uz="O'qishning boshlanishi",
         text_ru="Начало учебного года",
         text_en="Academic year begins"),
]


DOCS = [
    dict(title_uz="Bakalavr uchun hujjatlar",
         title_ru="Документы для бакалавриата",
         title_en="Documents for Bachelor's",
         items=[
             {"uz":"Pasport nusxasi (2 ta)",
              "ru":"Копия паспорта (2 шт.)",
              "en":"Passport copy (2 copies)"},
             {"uz":"Attestat va o'rta ma'lumot haqida hujjat",
              "ru":"Аттестат и документ о среднем образовании",
              "en":"School certificate"},
             {"uz":"086-shakl tibbiy ma'lumotnoma",
              "ru":"Медицинская справка форма 086",
              "en":"Medical certificate (form 086)"},
             {"uz":"3×4 rasm (4 ta)",
              "ru":"Фото 3×4 (4 шт.)",
              "en":"3×4 photos (4 pieces)"},
             {"uz":"Universitet shakli ariza",
              "ru":"Заявление по форме университета",
              "en":"University application form"},
         ]),
    dict(title_uz="Magistratura uchun hujjatlar",
         title_ru="Документы для магистратуры",
         title_en="Documents for Master's",
         items=[
             {"uz":"Bakalavriat diplomi nusxasi","ru":"Копия диплома бакалавра","en":"Bachelor's diploma copy"},
             {"uz":"Pasport va boshqa shaxsiy hujjatlar","ru":"Паспорт и личные документы","en":"Passport and personal documents"},
             {"uz":"Imtihon natijalari (mavjud bo'lsa)","ru":"Результаты экзаменов (если есть)","en":"Exam results (if any)"},
         ]),
    dict(title_uz="Sirtqi ta'lim uchun hujjatlar",
         title_ru="Документы для заочного обучения",
         title_en="Documents for part-time",
         items=[
             {"uz":"Pasport nusxasi","ru":"Копия паспорта","en":"Passport copy"},
             {"uz":"Ish joyidan ma'lumotnoma","ru":"Справка с места работы","en":"Employment certificate"},
             {"uz":"Attestat","ru":"Аттестат","en":"School certificate"},
         ]),
]


FAQS = [
    dict(question_uz="Qabul qachon boshlanadi?", question_ru="Когда начинается приём?", question_en="When does admission start?",
         answer_uz="Qabul iyun oyidan sentabrgacha davom etadi. Eng erta hujjatlarni iyun boshida topshirishingiz mumkin.",
         answer_ru="Приём проходит с июня по сентябрь. Документы можно подать с начала июня.",
         answer_en="Admission runs from June to September. You can submit documents from early June."),
    dict(question_uz="Stipendiya berishadimi?", question_ru="Дают ли стипендию?", question_en="Are scholarships available?",
         answer_uz="Imtihon natijalariga ko'ra eng yaxshi talabalarga stipendiya tayinlanadi. Bundan tashqari, ijtimoiy yordam dasturlari ham mavjud.",
         answer_ru="Лучшим студентам по результатам экзаменов назначается стипендия. Также есть программы социальной поддержки.",
         answer_en="Top performers receive scholarships based on exam results. Social support programs are also available."),
    dict(question_uz="Chet ellik talabalar qabul qilinadimi?", question_ru="Принимают ли иностранных студентов?", question_en="Do you accept international students?",
         answer_uz="Ha, xalqaro talabalar uchun maxsus qabul dasturlari va yotoqxona xizmati mavjud.",
         answer_ru="Да, для иностранных студентов есть специальные программы приёма и общежитие.",
         answer_en="Yes, we have dedicated admission programs and dormitory services for international students."),
    dict(question_uz="Onlayn imtihon mavjudmi?", question_ru="Есть ли онлайн-экзамен?", question_en="Is there an online exam?",
         answer_uz="Bir necha yo'nalishda onlayn test imkoniyati mavjud, lekin asosan an'anaviy yozma test o'tkaziladi.",
         answer_ru="Для нескольких направлений доступен онлайн-тест, но в основном проводится письменный экзамен.",
         answer_en="A few programs offer online tests, but most use traditional written exams."),
    dict(question_uz="Yotoqxona berishadimi?", question_ru="Предоставляют ли общежитие?", question_en="Is dormitory provided?",
         answer_uz="Boshqa shahardan kelgan talabalar uchun zamonaviy yotoqxona xonalari ajratiladi (mavjudligi va navbat asosida).",
         answer_ru="Иногородним студентам предоставляются современные комнаты в общежитии (в порядке очереди).",
         answer_en="Modern dormitory rooms are allocated for students from other regions (subject to availability)."),
]


async def seed_collection(session, model, rows, label):
    if (await session.execute(select(model))).first():
        return
    for i, r in enumerate(rows):
        session.add(model(sort_order=i, enabled=True, **r))
    print(f"  {len(rows)} {label} seeded")


async def main():
    async with AsyncSessionLocal() as session:
        print("=== Seeding Applicants page ===")
        await upsert_page(session)
        await seed_collection(session, ApplicantsStep,         STEPS,    "steps")
        await seed_collection(session, ApplicantsForm,         FORMS,    "forms")
        await seed_collection(session, ApplicantsTimelineItem, TIMELINE, "timeline items")
        await seed_collection(session, ApplicantsDocCategory,  DOCS,     "doc categories")
        await seed_collection(session, ApplicantsFaq,          FAQS,     "faqs")
        await session.commit()
        print("=== Done ===")


if __name__ == "__main__":
    asyncio.run(main())
