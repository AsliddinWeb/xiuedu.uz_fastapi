"""
Index all CMS content into chat_content_chunks for RAG retrieval.

Each chunk = one logical piece of content (program info, FAQ answer,
contact info, etc.) with source metadata. Tsvector is auto-built
by a trigger or inline via to_tsvector().

Call `reindex_all(session)` after any admin content update,
or run `scripts/index_chat_content.py` as a one-shot.
"""
import re
from sqlalchemy import delete, select
from sqlalchemy import text as sa_text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chat import ContentChunk
from app.models.home_settings import (
    Faculty, FacultyProgram, AdmissionStep, Stat, Testimonial,
    Partner, License, HomeFAQ, WhyCard, QuickAction, IntroPillar
)
from app.models.leader import Leader
from app.models.about_page import AboutPage, TimelineEvent, Accreditation
from app.models.applicants_page import (
    ApplicantsPage, ApplicantsStep, ApplicantsForm, ApplicantsFaq,
    ApplicantsTimelineItem, ApplicantsDocCategory
)
from app.models.contact_page import ContactPage
from app.models.vacancies_page import Vacancy
from app.models.international_page import IntlProgram, IntlPartner

STRIP_HTML = re.compile(r"<[^>]+>")


def strip(text: str | None) -> str:
    if not text:
        return ""
    return STRIP_HTML.sub(" ", text).strip()


def _chunk(source_type: str, source_id: str, source_label: str, lang: str, content: str) -> ContentChunk | None:
    content = strip(content)
    if not content or len(content) < 10:
        return None
    return ContentChunk(
        source_type=source_type,
        source_id=str(source_id),
        source_label=source_label,
        lang=lang,
        content=content,
    )


def _add(chunks: list, *args):
    c = _chunk(*args)
    if c:
        chunks.append(c)


async def reindex_all(session: AsyncSession):
    """Drop all chunks and rebuild from CMS tables."""
    await session.execute(delete(ContentChunk))
    chunks: list[ContentChunk] = []

    # ── Faculties + programs ──
    faculties = (await session.execute(select(Faculty))).scalars().all()
    programs = (await session.execute(select(FacultyProgram))).scalars().all()

    fac_map = {f.id: f for f in faculties}
    for p in programs:
        fac = fac_map.get(p.faculty_id)
        fac_name = fac.name_uz if fac else ""
        for lang in ("uz", "ru", "en"):
            name = getattr(p, f"name_{lang}", "")
            dur = getattr(p, f"duration_{lang}", "")
            lang_field = getattr(p, f"language_{lang}", "")
            degree = getattr(p, f"degree_{lang}", "")
            forms_info = ""
            for sf in (p.study_forms or []):
                form_type = sf.get("form", "")
                tuition = sf.get("tuition", "")
                seats = sf.get("seats", "")
                forms_info += f" {form_type}: {tuition} ({seats} o'rin)."

            text = f"{name}. {fac_name}. {dur}. {lang_field}. {degree}. {p.credits or ''} kredit.{forms_info}"
            _add(chunks, "program", str(p.id), name, lang, text)

    for f in faculties:
        for lang in ("uz", "ru", "en"):
            _add(chunks, "faculty", f.slug, getattr(f, f"name_{lang}", ""),
                 lang, f"{getattr(f, f'name_{lang}', '')}. {getattr(f, f'description_{lang}', '')}")

    # ── Leaders ──
    leaders = (await session.execute(select(Leader))).scalars().all()
    for l in leaders:
        for lang in ("uz", "ru", "en"):
            _add(chunks, "leader", str(l.id), getattr(l, f"name_{lang}", ""),
                 lang, f"{getattr(l, f'name_{lang}', '')}. {getattr(l, f'position_{lang}', '')}. {getattr(l, f'degree_{lang}', '')}. {getattr(l, f'bio_{lang}', '')}. {l.email or ''}")

    # ── About ──
    about = (await session.execute(select(AboutPage).limit(1))).scalar_one_or_none()
    if about:
        for lang in ("uz", "ru", "en"):
            mission = getattr(about, f"mission_{lang}", "") or ""
            vision = getattr(about, f"vision_{lang}", "") or ""
            values = getattr(about, f"values_{lang}", "") or ""
            _add(chunks, "about", "mvv", "Mission/Vision/Values",
                 lang, f"Missiya: {mission}. Vizyon: {vision}. Qadriyatlar: {values}.")
            for i, para in enumerate(about.rector_letter_paragraphs or []):
                text = para.get(lang, "") if isinstance(para, dict) else ""
                _add(chunks, "about", f"rector_{i}", "Rektor murojaati", lang, text)

    # ── FAQs (home + applicants) ──
    home_faqs = (await session.execute(select(HomeFAQ))).scalars().all()
    for f in home_faqs:
        for lang in ("uz", "ru", "en"):
            q = getattr(f, f"question_{lang}", "")
            a = getattr(f, f"answer_{lang}", "")
            _add(chunks, "faq", str(f.id), q, lang, f"Savol: {q}. Javob: {a}")

    app_faqs = (await session.execute(select(ApplicantsFaq))).scalars().all()
    for f in app_faqs:
        for lang in ("uz", "ru", "en"):
            q = getattr(f, f"question_{lang}", "")
            a = getattr(f, f"answer_{lang}", "")
            _add(chunks, "applicant_faq", str(f.id), q, lang, f"Savol: {q}. Javob: {a}")

    # ── Admission steps ──
    adm_steps = (await session.execute(select(ApplicantsStep))).scalars().all()
    for s in adm_steps:
        for lang in ("uz", "ru", "en"):
            _add(chunks, "admission_step", str(s.id), getattr(s, f"title_{lang}", ""),
                 lang, f"{getattr(s, f'title_{lang}', '')}. {getattr(s, f'desc_{lang}', '')}")

    # ── Contact ──
    contact = (await session.execute(select(ContactPage).limit(1))).scalar_one_or_none()
    if contact:
        for lang in ("uz", "ru", "en"):
            addr = getattr(contact, f"address_{lang}", "") or ""
            hours = getattr(contact, f"working_hours_{lang}", "") or ""
            _add(chunks, "contact", "info", "Aloqa",
                 lang, f"Manzil: {addr}. Telefon: {contact.phone or ''}. Email: {contact.email or ''}. Ish vaqti: {hours}.")

    # ── Vacancies ──
    vacancies = (await session.execute(select(Vacancy).where(Vacancy.enabled.is_(True)))).scalars().all()
    for v in vacancies:
        for lang in ("uz", "ru", "en"):
            title = getattr(v, f"title_{lang}", "")
            dept = getattr(v, f"department_{lang}", "")
            desc = getattr(v, f"description_{lang}", "")
            req = getattr(v, f"requirements_{lang}", "")
            _add(chunks, "vacancy", str(v.id), title,
                 lang, f"Vakansiya: {title}. Bo'lim: {dept}. {desc}. Talablar: {req}. Maosh: {v.salary or ''}.")

    # ── Stats (numbers) ──
    stats = (await session.execute(select(Stat))).scalars().all()
    for s in stats:
        for lang in ("uz", "ru", "en"):
            _add(chunks, "stat", str(s.id), getattr(s, f"label_{lang}", ""),
                 lang, f"{s.value} — {getattr(s, f'label_{lang}', '')}. {getattr(s, f'sub_{lang}', '')}")

    # ── International programs ──
    intl_progs = (await session.execute(select(IntlProgram))).scalars().all()
    for p in intl_progs:
        for lang in ("uz", "ru", "en"):
            _add(chunks, "intl_program", str(p.id), getattr(p, f"title_{lang}", ""),
                 lang, f"{getattr(p, f'title_{lang}', '')}. {getattr(p, f'desc_{lang}', '')}")

    # Bulk insert
    session.add_all(chunks)
    await session.flush()

    # Build tsvector using multi-language config
    await session.execute(sa_text("""
        UPDATE chat_content_chunks
        SET tsv = to_tsvector('simple', content)
        WHERE tsv IS NULL
    """))

    await session.commit()
    return len(chunks)
