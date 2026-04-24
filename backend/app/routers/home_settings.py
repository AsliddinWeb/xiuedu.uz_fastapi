"""
Home page CMS routers.

Public:
    GET  /api/page-settings/home              — full localized payload
    GET  /api/faculties/                      — public faculty list

Admin (admin | content_manager):
    Hero / Sections / Campus / FinalCTA — singleton-style PUT
    QuickAction / IntroPillar / WhyCard / Faculty / FacultyProgram /
        AdmissionStep / Stat / Testimonial / Partner / License / HomeFAQ
        — full CRUD
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.home_settings import (
    AdmissionStep, CampusSection, Faculty, FacultyProgram, FinalCTA, HeroSettings,
    HomeFAQ, HomeSection, IntroPillar, License, Partner, QuickAction, Stat,
    Testimonial, WhyCard,
)
from app.models.user import Role, User
from app.schemas.home_settings import (
    AdmissionStepAdminOut, AdmissionStepCreate, AdmissionStepPublicOut, AdmissionStepUpdate,
    CampusAdminOut, CampusPublicOut, CampusUpdate,
    FacultyAdminOut, FacultyCreate, FacultyProgramAdminOut, FacultyProgramCreate,
    FacultyProgramPublicOut, FacultyProgramUpdate, FacultyPublicOut, FacultyUpdate, StudyFormOut,
    FinalCTAAdminOut, FinalCTAPublicOut, FinalCTAUpdate,
    HeroAdminOut, HeroPublicOut, HeroUpdate,
    HomeFAQAdminOut, HomeFAQCreate, HomeFAQPublicOut, HomeFAQUpdate,
    HomePagePublic,
    IntroPillarAdminOut, IntroPillarCreate, IntroPillarPublicOut, IntroPillarUpdate,
    LicenseAdminOut, LicenseCreate, LicensePublicOut, LicenseUpdate,
    PartnerAdminOut, PartnerCreate, PartnerPublicOut, PartnerUpdate,
    QuickActionAdminOut, QuickActionCreate, QuickActionPublicOut, QuickActionUpdate,
    SectionAdminOut, SectionPublicOut, SectionUpdate,
    StatAdminOut, StatCreate, StatPublicOut, StatUpdate,
    TestimonialAdminOut, TestimonialCreate, TestimonialPublicOut, TestimonialUpdate,
    WhyCardAdminOut, WhyCardCreate, WhyCardPublicOut, WhyCardUpdate,
)
from app.utils.deps import require_roles
from app.utils.lang import Lang, get_lang, pick

# ─────────────────────────────────────────────────────────────────
#  Public router
# ─────────────────────────────────────────────────────────────────
public = APIRouter(prefix="/page-settings", tags=["page-settings"])
faculties_public = APIRouter(prefix="/faculties", tags=["faculties"])


def _hero_public(h: HeroSettings | None, lang: Lang) -> HeroPublicOut | None:
    if not h:
        return None
    return HeroPublicOut(
        variant=h.variant,
        enabled=h.enabled,
        eyebrow=pick(h, "eyebrow", lang),
        title=pick(h, "title", lang),
        title_highlight=pick(h, "title_highlight", lang),
        title_tail=pick(h, "title_tail", lang),
        subtitle=pick(h, "subtitle", lang),
        bg_image=h.bg_image,
        bg_video=h.bg_video,
        bg_video_poster=h.bg_video_poster,
        side_image=h.side_image,
        overlay_opacity=h.overlay_opacity,
        cta_primary_label=pick(h, "cta_primary_label", lang),
        cta_primary_url=h.cta_primary_url,
        cta_primary_external=h.cta_primary_external,
        cta_secondary_label=pick(h, "cta_secondary_label", lang),
        cta_secondary_url=h.cta_secondary_url,
        cta_secondary_external=h.cta_secondary_external,
        show_particles=h.show_particles,
        show_scroll_indicator=h.show_scroll_indicator,
        show_trust_badges=h.show_trust_badges,
        show_floating_cards=h.show_floating_cards,
        quote_text=pick(h, "quote_text", lang),
        quote_author=pick(h, "quote_author", lang),
        badge1_value=h.badge1_value,
        badge1_label=pick(h, "badge1_label", lang),
        badge1_icon=h.badge1_icon,
        badge2_value=h.badge2_value,
        badge2_label=pick(h, "badge2_label", lang),
        badge2_icon=h.badge2_icon,
        trust_badges=[
            {"label": b.get("label", ""), "sub": b.get(f"sub_{lang}") or b.get("sub_uz", ""), "icon": b.get("icon", "ShieldCheckIcon")}
            for b in (h.trust_badges or [])
        ],
    )


def _section_public(s: HomeSection, lang: Lang) -> SectionPublicOut:
    return SectionPublicOut(
        key=s.key,
        enabled=s.enabled,
        sort_order=s.sort_order,
        eyebrow=pick(s, "eyebrow", lang),
        title=pick(s, "title", lang),
        subtitle=pick(s, "subtitle", lang),
        body_p1=pick(s, "body_p1", lang),
        body_p2=pick(s, "body_p2", lang),
        link_label=pick(s, "link_label", lang),
        link_url=s.link_url,
        settings=s.settings or {},
    )


def _campus_public(c: CampusSection | None, lang: Lang) -> CampusPublicOut | None:
    if not c:
        return None
    bullets = []
    for b in (c.bullets or []):
        if isinstance(b, dict):
            bullets.append(b.get(lang) or b.get("uz") or "")
    return CampusPublicOut(
        main_image=c.main_image,
        image_2=c.image_2,
        image_3=c.image_3,
        video_url=c.video_url,
        eyebrow=pick(c, "eyebrow", lang),
        title=pick(c, "title", lang),
        text=pick(c, "text", lang),
        bullets=[b for b in bullets if b],
        cta_label=pick(c, "cta_label", lang),
        cta_url=c.cta_url,
    )


def _final_cta_public(c: FinalCTA | None, lang: Lang) -> FinalCTAPublicOut | None:
    if not c:
        return None
    return FinalCTAPublicOut(
        enabled=c.enabled,
        eyebrow=pick(c, "eyebrow", lang),
        title=pick(c, "title", lang),
        text=pick(c, "text", lang),
        cta_label=pick(c, "cta_label", lang),
        cta_url=c.cta_url,
        cta_external=c.cta_external,
        phone_label=c.phone_label,
        phone_url=c.phone_url,
    )


def _faculty_public(f: Faculty, lang: Lang) -> FacultyPublicOut:
    return FacultyPublicOut(
        id=f.id,
        slug=f.slug,
        icon=f.icon,
        name=pick(f, "name", lang) or "",
        description=pick(f, "description", lang) or "",
        cover_image=f.cover_image,
        programs=[
            FacultyProgramPublicOut(
                id=p.id,
                level=p.level,
                study_forms=[
                    StudyFormOut(form=sf.get("form", "full_time"), tuition=sf.get("tuition", ""), seats=sf.get("seats"))
                    for sf in (p.study_forms or [])
                ] or [StudyFormOut(form=p.study_form, tuition=p.tuition, seats=p.seats)],
                name=pick(p, "name", lang) or "",
                icon=p.icon,
                bg_class=p.bg_class,
                icon_bg_class=p.icon_bg_class,
                ring_class=p.ring_class,
                duration=pick(p, "duration", lang) or "",
                language=pick(p, "language", lang) or "",
                degree=pick(p, "degree", lang) or "",
                credits=p.credits,
            )
            for p in f.programs if p.enabled
        ],
    )


@public.get("/home", response_model=HomePagePublic)
async def get_home_settings(
    db: Annotated[AsyncSession, Depends(get_db)],
    lang: Annotated[Lang, Depends(get_lang)],
):
    hero = (await db.execute(
        select(HeroSettings).where(HeroSettings.page == "home")
    )).scalar_one_or_none()

    sections = (await db.execute(
        select(HomeSection).order_by(HomeSection.sort_order, HomeSection.id)
    )).scalars().all()

    qas = (await db.execute(
        select(QuickAction).where(QuickAction.enabled.is_(True))
                           .order_by(QuickAction.sort_order, QuickAction.id)
    )).scalars().all()

    pillars = (await db.execute(
        select(IntroPillar).where(IntroPillar.enabled.is_(True))
                           .order_by(IntroPillar.sort_order, IntroPillar.id)
    )).scalars().all()

    campus = (await db.execute(select(CampusSection).limit(1))).scalar_one_or_none()

    why = (await db.execute(
        select(WhyCard).where(WhyCard.enabled.is_(True))
                       .order_by(WhyCard.sort_order, WhyCard.id)
    )).scalars().all()

    facs = (await db.execute(
        select(Faculty).where(Faculty.enabled.is_(True))
                       .options(selectinload(Faculty.programs))
                       .order_by(Faculty.sort_order, Faculty.id)
    )).scalars().all()

    steps = (await db.execute(
        select(AdmissionStep).where(AdmissionStep.enabled.is_(True))
                             .order_by(AdmissionStep.sort_order, AdmissionStep.id)
    )).scalars().all()

    stats = (await db.execute(
        select(Stat).where(Stat.enabled.is_(True))
                    .order_by(Stat.sort_order, Stat.id)
    )).scalars().all()

    testimonials = (await db.execute(
        select(Testimonial).where(Testimonial.enabled.is_(True))
                           .order_by(Testimonial.sort_order, Testimonial.id)
    )).scalars().all()

    partners = (await db.execute(
        select(Partner).where(Partner.enabled.is_(True))
                       .order_by(Partner.sort_order, Partner.id)
    )).scalars().all()

    licenses = (await db.execute(
        select(License).where(License.enabled.is_(True))
                       .order_by(License.sort_order, License.id)
    )).scalars().all()

    faqs = (await db.execute(
        select(HomeFAQ).where(HomeFAQ.enabled.is_(True))
                       .order_by(HomeFAQ.sort_order, HomeFAQ.id)
    )).scalars().all()

    cta = (await db.execute(select(FinalCTA).limit(1))).scalar_one_or_none()

    return HomePagePublic(
        hero=_hero_public(hero, lang),
        sections=[_section_public(s, lang) for s in sections],
        quick_actions=[
            QuickActionPublicOut(
                id=q.id, icon=q.icon,
                title=pick(q, "title", lang) or "",
                desc=pick(q, "desc", lang) or "",
                url=q.url, external=q.external, accent=q.accent,
            ) for q in qas
        ],
        intro_pillars=[
            IntroPillarPublicOut(
                id=p.id, icon=p.icon,
                title=pick(p, "title", lang) or "",
                desc=pick(p, "desc", lang) or "",
            ) for p in pillars
        ],
        campus=_campus_public(campus, lang),
        why_cards=[
            WhyCardPublicOut(
                id=w.id, icon=w.icon, icon_bg=w.icon_bg, icon_color=w.icon_color,
                number=w.number,
                number_label=pick(w, "number_label", lang) or "",
                title=pick(w, "title", lang) or "",
                desc=pick(w, "desc", lang) or "",
            ) for w in why
        ],
        faculties=[_faculty_public(f, lang) for f in facs],
        admission_steps=[
            AdmissionStepPublicOut(
                id=s.id, number=s.number, icon=s.icon,
                title=pick(s, "title", lang) or "",
                desc=pick(s, "desc", lang) or "",
            ) for s in steps
        ],
        stats=[
            StatPublicOut(
                id=s.id, value=s.value,
                label=pick(s, "label", lang) or "",
                sub=pick(s, "sub", lang) or "",
            ) for s in stats
        ],
        testimonials=[
            TestimonialPublicOut(
                id=t.id,
                name=pick(t, "name", lang) or "",
                role=pick(t, "role", lang) or "",
                text=pick(t, "text", lang) or "",
                avatar=t.avatar, rating=t.rating, year=t.year,
            ) for t in testimonials
        ],
        partners=[
            PartnerPublicOut(
                id=p.id, flag=p.flag,
                country=pick(p, "country", lang) or "",
                count=p.count, logo_url=p.logo_url, url=p.url,
            ) for p in partners
        ],
        licenses=[
            LicensePublicOut(
                id=l.id,
                title=pick(l, "title", lang) or "",
                issuer=pick(l, "issuer", lang) or "",
                year=l.year, image=l.image, pdf=l.pdf,
            ) for l in licenses
        ],
        faqs=[
            HomeFAQPublicOut(
                id=q.id,
                question=pick(q, "question", lang) or "",
                answer=pick(q, "answer", lang) or "",
            ) for q in faqs
        ],
        final_cta=_final_cta_public(cta, lang),
    )


@faculties_public.get("/", response_model=list[FacultyPublicOut])
async def list_faculties(
    db: Annotated[AsyncSession, Depends(get_db)],
    lang: Annotated[Lang, Depends(get_lang)],
):
    rows = (await db.execute(
        select(Faculty).where(Faculty.enabled.is_(True))
                       .options(selectinload(Faculty.programs))
                       .order_by(Faculty.sort_order, Faculty.id)
    )).scalars().all()
    return [_faculty_public(f, lang) for f in rows]


@faculties_public.get("/{slug}", response_model=FacultyPublicOut)
async def get_faculty(
    slug: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    lang: Annotated[Lang, Depends(get_lang)],
):
    f = (await db.execute(
        select(Faculty).where(Faculty.slug == slug, Faculty.enabled.is_(True))
                       .options(selectinload(Faculty.programs))
    )).scalar_one_or_none()
    if not f:
        raise HTTPException(404, "Faculty not found")
    return _faculty_public(f, lang)


# ─────────────────────────────────────────────────────────────────
#  Admin router
# ─────────────────────────────────────────────────────────────────
admin = APIRouter(prefix="/admin/home", tags=["admin:home"])
_dep = require_roles(Role.ADMIN, Role.CONTENT_MANAGER)


# ── Hero (singleton by page) ──
@admin.get("/hero", response_model=HeroAdminOut)
async def admin_get_hero(
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    h = (await db.execute(
        select(HeroSettings).where(HeroSettings.page == "home")
    )).scalar_one_or_none()
    if not h:
        h = HeroSettings(page="home")
        db.add(h)
        await db.commit()
        await db.refresh(h)
    return h


@admin.put("/hero", response_model=HeroAdminOut)
async def admin_update_hero(
    payload: HeroUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    h = (await db.execute(
        select(HeroSettings).where(HeroSettings.page == "home")
    )).scalar_one_or_none()
    if not h:
        h = HeroSettings(page="home")
        db.add(h)
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(h, k, v)
    await db.commit()
    await db.refresh(h)
    return h


# ── Sections (no insert/delete — keys come from seed) ──
@admin.get("/sections", response_model=list[SectionAdminOut])
async def admin_list_sections(
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    rows = (await db.execute(
        select(HomeSection).order_by(HomeSection.sort_order, HomeSection.id)
    )).scalars().all()
    return rows


@admin.put("/sections/{key}", response_model=SectionAdminOut)
async def admin_update_section(
    key: str,
    payload: SectionUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    s = (await db.execute(
        select(HomeSection).where(HomeSection.key == key)
    )).scalar_one_or_none()
    if not s:
        raise HTTPException(404, "Section not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(s, k, v)
    await db.commit()
    await db.refresh(s)
    return s


# ── Generic CRUD factory to avoid 100 lines of repetition ──
def _crud(model, base_path: str, out_schema, create_schema, update_schema, *,
          ordered: bool = True):
    @admin.get(f"/{base_path}", response_model=list[out_schema], name=f"list_{base_path}")
    async def _list(
        db: Annotated[AsyncSession, Depends(get_db)],
        _u: User = Depends(_dep),
    ):
        stmt = select(model)
        if ordered:
            stmt = stmt.order_by(model.sort_order, model.id)
        return (await db.execute(stmt)).scalars().all()

    @admin.post(f"/{base_path}", response_model=out_schema, status_code=201, name=f"create_{base_path}")
    async def _create(
        payload: create_schema,
        db: Annotated[AsyncSession, Depends(get_db)],
        _u: User = Depends(_dep),
    ):
        obj = model(**payload.model_dump())
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    @admin.put(f"/{base_path}/{{item_id}}", response_model=out_schema, name=f"update_{base_path}")
    async def _update(
        item_id: int,
        payload: update_schema,
        db: Annotated[AsyncSession, Depends(get_db)],
        _u: User = Depends(_dep),
    ):
        obj = await db.get(model, item_id)
        if not obj:
            raise HTTPException(404, "Not found")
        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(obj, k, v)
        await db.commit()
        await db.refresh(obj)
        return obj

    @admin.delete(f"/{base_path}/{{item_id}}", status_code=204, name=f"delete_{base_path}")
    async def _delete(
        item_id: int,
        db: Annotated[AsyncSession, Depends(get_db)],
        _u: User = Depends(_dep),
    ):
        obj = await db.get(model, item_id)
        if not obj:
            raise HTTPException(404, "Not found")
        await db.delete(obj)
        await db.commit()


_crud(QuickAction,    "quick-actions",   QuickActionAdminOut,   QuickActionCreate,   QuickActionUpdate)
_crud(IntroPillar,    "intro-pillars",   IntroPillarAdminOut,   IntroPillarCreate,   IntroPillarUpdate)
_crud(WhyCard,        "why-cards",       WhyCardAdminOut,       WhyCardCreate,       WhyCardUpdate)
_crud(AdmissionStep,  "admission-steps", AdmissionStepAdminOut, AdmissionStepCreate, AdmissionStepUpdate)
_crud(Stat,           "stats",           StatAdminOut,          StatCreate,          StatUpdate)
_crud(Testimonial,    "testimonials",    TestimonialAdminOut,   TestimonialCreate,   TestimonialUpdate)
_crud(Partner,        "partners",        PartnerAdminOut,       PartnerCreate,       PartnerUpdate)
_crud(License,        "licenses",        LicenseAdminOut,       LicenseCreate,       LicenseUpdate)
_crud(HomeFAQ,        "faqs",            HomeFAQAdminOut,       HomeFAQCreate,       HomeFAQUpdate)


# ── Faculties (slug uniqueness + nested programs) ──
@admin.get("/faculties", response_model=list[FacultyAdminOut])
async def admin_list_faculties(
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    rows = (await db.execute(
        select(Faculty).options(selectinload(Faculty.programs))
                       .order_by(Faculty.sort_order, Faculty.id)
    )).scalars().all()
    return rows


@admin.get("/faculties/{faculty_id}", response_model=FacultyAdminOut)
async def admin_get_faculty(
    faculty_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    f = (await db.execute(
        select(Faculty).where(Faculty.id == faculty_id)
                       .options(selectinload(Faculty.programs))
    )).scalar_one_or_none()
    if not f:
        raise HTTPException(404, "Faculty not found")
    return f


@admin.post("/faculties", response_model=FacultyAdminOut, status_code=201)
async def admin_create_faculty(
    payload: FacultyCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    if (await db.execute(select(Faculty).where(Faculty.slug == payload.slug))).scalar_one_or_none():
        raise HTTPException(409, "Slug already exists")
    f = Faculty(**payload.model_dump())
    db.add(f)
    await db.commit()
    f = (await db.execute(
        select(Faculty).where(Faculty.id == f.id).options(selectinload(Faculty.programs))
    )).scalar_one()
    return f


@admin.put("/faculties/{faculty_id}", response_model=FacultyAdminOut)
async def admin_update_faculty(
    faculty_id: int,
    payload: FacultyUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    f = await db.get(Faculty, faculty_id)
    if not f:
        raise HTTPException(404, "Faculty not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(f, k, v)
    await db.commit()
    f = (await db.execute(
        select(Faculty).where(Faculty.id == faculty_id).options(selectinload(Faculty.programs))
    )).scalar_one()
    return f


@admin.delete("/faculties/{faculty_id}", status_code=204)
async def admin_delete_faculty(
    faculty_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    f = await db.get(Faculty, faculty_id)
    if not f:
        raise HTTPException(404, "Faculty not found")
    await db.delete(f)
    await db.commit()


# ── Faculty programs nested CRUD ──
@admin.post("/faculties/{faculty_id}/programs", response_model=FacultyProgramAdminOut, status_code=201)
async def admin_create_program(
    faculty_id: int,
    payload: FacultyProgramCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    if not await db.get(Faculty, faculty_id):
        raise HTTPException(404, "Faculty not found")
    p = FacultyProgram(faculty_id=faculty_id, **payload.model_dump())
    db.add(p)
    await db.commit()
    await db.refresh(p)
    return p


@admin.put("/programs/{program_id}", response_model=FacultyProgramAdminOut)
async def admin_update_program(
    program_id: int,
    payload: FacultyProgramUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    p = await db.get(FacultyProgram, program_id)
    if not p:
        raise HTTPException(404, "Program not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(p, k, v)
    await db.commit()
    await db.refresh(p)
    return p


@admin.delete("/programs/{program_id}", status_code=204)
async def admin_delete_program(
    program_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    p = await db.get(FacultyProgram, program_id)
    if not p:
        raise HTTPException(404, "Program not found")
    await db.delete(p)
    await db.commit()


# ── Campus (singleton) ──
@admin.get("/campus", response_model=CampusAdminOut)
async def admin_get_campus(
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    c = (await db.execute(select(CampusSection).limit(1))).scalar_one_or_none()
    if not c:
        c = CampusSection(bullets=[])
        db.add(c)
        await db.commit()
        await db.refresh(c)
    return c


@admin.put("/campus", response_model=CampusAdminOut)
async def admin_update_campus(
    payload: CampusUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    c = (await db.execute(select(CampusSection).limit(1))).scalar_one_or_none()
    if not c:
        c = CampusSection(bullets=[])
        db.add(c)
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(c, k, v)
    await db.commit()
    await db.refresh(c)
    return c


# ── Final CTA (singleton) ──
@admin.get("/final-cta", response_model=FinalCTAAdminOut)
async def admin_get_final_cta(
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    c = (await db.execute(select(FinalCTA).limit(1))).scalar_one_or_none()
    if not c:
        c = FinalCTA()
        db.add(c)
        await db.commit()
        await db.refresh(c)
    return c


@admin.put("/final-cta", response_model=FinalCTAAdminOut)
async def admin_update_final_cta(
    payload: FinalCTAUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    c = (await db.execute(select(FinalCTA).limit(1))).scalar_one_or_none()
    if not c:
        c = FinalCTA()
        db.add(c)
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(c, k, v)
    await db.commit()
    await db.refresh(c)
    return c
