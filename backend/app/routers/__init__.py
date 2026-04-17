from fastapi import APIRouter

from app.routers.auth import router as auth_router
from app.routers.chat import router as chat_router
from app.routers.site_settings import admin as site_settings_admin
from app.routers.site_settings import public as site_settings_public
from app.routers.contact import router as contact_router
from app.routers.event import admin as events_admin
from app.routers.event import public as events_public
from app.routers.home_settings import admin as home_admin
from app.routers.home_settings import faculties_public as faculties_router
from app.routers.home_settings import public as home_public
from app.routers.leader import admin as leader_admin
from app.routers.leader import public as leader_public
from app.routers.about_page import admin as about_admin
from app.routers.about_page import public as about_public
from app.routers.applicants_page import admin as applicants_admin
from app.routers.applicants_page import public as applicants_public
from app.routers.structure_page import admin as structure_admin
from app.routers.structure_page import public as structure_public
from app.routers.international_page import admin as intl_admin
from app.routers.international_page import public as intl_public
from app.routers.vacancies_page import admin as vacancies_admin
from app.routers.vacancies_page import public as vacancies_public
from app.routers.contact_page import admin as contact_page_admin
from app.routers.contact_page import public as contact_page_public
from app.routers.gallery_page import admin as gallery_admin
from app.routers.gallery_page import public as gallery_public
from app.routers.media import router as media_router
from app.routers.news import admin_cat as news_admin_cat
from app.routers.news import admin_news as news_admin
from app.routers.news import public as news_public
from app.routers.pages import admin as pages_admin
from app.routers.pages import public as pages_public
from app.routers.seo import admin as seo_admin
from app.routers.seo import public as seo_public
from app.routers.stats import router as stats_router
from app.routers.users import router as users_router

api_router = APIRouter()

# Auth
api_router.include_router(auth_router)

# Public content
api_router.include_router(pages_public)
api_router.include_router(news_public)
api_router.include_router(events_public)
api_router.include_router(seo_public)
api_router.include_router(contact_router)
api_router.include_router(home_public)
api_router.include_router(faculties_router)
api_router.include_router(leader_public)
api_router.include_router(about_public)
api_router.include_router(applicants_public)
api_router.include_router(structure_public)
api_router.include_router(intl_public)
api_router.include_router(vacancies_public)
api_router.include_router(contact_page_public)
api_router.include_router(gallery_public)
api_router.include_router(chat_router)
api_router.include_router(site_settings_public)

# Admin
api_router.include_router(pages_admin)
api_router.include_router(news_admin)
api_router.include_router(news_admin_cat)
api_router.include_router(events_admin)
api_router.include_router(media_router)
api_router.include_router(users_router)
api_router.include_router(seo_admin)
api_router.include_router(stats_router)
api_router.include_router(home_admin)
api_router.include_router(leader_admin)
api_router.include_router(about_admin)
api_router.include_router(applicants_admin)
api_router.include_router(structure_admin)
api_router.include_router(intl_admin)
api_router.include_router(vacancies_admin)
api_router.include_router(contact_page_admin)
api_router.include_router(site_settings_admin)
api_router.include_router(gallery_admin)


@api_router.get("/", tags=["root"])
async def root():
    return {
        "name": "XIU Edu API",
        "version": "2.0.0",
        "docs": "/api/docs",
    }
