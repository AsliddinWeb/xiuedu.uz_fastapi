from app.models.user import User, Role  # noqa: F401
from app.models.page import StaticPage  # noqa: F401
from app.models.news import News, NewsCategory  # noqa: F401
from app.models.event import Event  # noqa: F401
from app.models.media import MediaFile  # noqa: F401
from app.models.seo import GlobalSEO, Redirect  # noqa: F401
from app.models.home_settings import (  # noqa: F401
    HeroSettings, HomeSection, QuickAction, IntroPillar, CampusSection,
    WhyCard, Faculty, FacultyProgram, AdmissionStep, Stat, Testimonial,
    Partner, License, HomeFAQ, FinalCTA,
)
from app.models.leader import Leader  # noqa: F401
from app.models.about_page import AboutPage, TimelineEvent, Accreditation  # noqa: F401
from app.models.applicants_page import (  # noqa: F401
    ApplicantsPage, ApplicantsStep, ApplicantsForm,
    ApplicantsTimelineItem, ApplicantsDocCategory, ApplicantsFaq,
)
from app.models.structure_page import StructurePage, AdminDepartment, SupportService  # noqa: F401
from app.models.international_page import InternationalPage, IntlProgram, IntlPartner  # noqa: F401
from app.models.vacancies_page import VacanciesPage, Vacancy  # noqa: F401
from app.models.contact_page import ContactPage  # noqa: F401
from app.models.gallery_page import GalleryPage, GalleryCategory, GalleryItem  # noqa: F401
from app.models.chat import ContentChunk, ChatMessage  # noqa: F401
from app.models.site_settings import SiteSettings  # noqa: F401
