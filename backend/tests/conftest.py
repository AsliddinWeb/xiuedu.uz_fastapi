"""
Pytest fixtures: in-memory SQLite + AsyncClient + role-based test users.
"""
import asyncio
import os

import pytest
import pytest_asyncio

# Force a sqlite test DB BEFORE app modules import
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["REDIS_URL"] = "redis://localhost:6379/15"
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["ALLOWED_ORIGINS"] = "http://localhost"

from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app import database as db_mod
from app.database import Base
from app.main import app
from app.models import news, page, user as user_model  # noqa: F401 register
from app.models.news import News, NewsCategory
from app.models.page import StaticPage
from app.models.user import Role, User
from app.utils.security import hash_password


# ===== Replace engine with sqlite test engine =====

test_engine = create_async_engine(
    os.environ["DATABASE_URL"],
    connect_args={"check_same_thread": False},
)
TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)
db_mod.engine = test_engine
db_mod.AsyncSessionLocal = TestSessionLocal


async def override_get_db():
    async with TestSessionLocal() as s:
        yield s


from app.database import get_db
app.dependency_overrides[get_db] = override_get_db


# ===== Patch redis blacklist to a no-op so tests don't need a server =====

class _FakeRedis:
    async def setex(self, *a, **k): return None
    async def exists(self, *a, **k): return 0
    async def lpush(self, *a, **k): return 1
    async def ltrim(self, *a, **k): return True
    async def get(self, *a, **k): return None
    def scan_iter(self, *a, **k):
        async def _empty():
            if False: yield
        return _empty()
    async def delete(self, *a, **k): return 0


from app import redis_client as rc_mod
from app.services import auth_service as auth_mod
from app.middleware import cache as cache_mod

_fake = _FakeRedis()
rc_mod.redis_client = _fake
auth_mod.redis_client = _fake
cache_mod.redis_client = _fake


# ===== Patch slowapi limiter to in-memory storage =====
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.middleware import rate_limit as rl_mod

_test_limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100000/minute"],
    storage_uri="memory://",
)
rl_mod.limiter = _test_limiter
app.state.limiter = _test_limiter


# ===== Schema lifecycle =====

@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def _create_schema():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def session() -> AsyncSession:
    async with TestSessionLocal() as s:
        yield s
        # Clean tables between tests
        for table in reversed(Base.metadata.sorted_tables):
            await s.execute(table.delete())
        await s.commit()


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# ===== User fixtures (one per role) =====

async def _make_user(session, email: str, role: Role, password: str = "TestPass123!") -> User:
    u = User(
        email=email,
        hashed_password=hash_password(password),
        full_name=f"Test {role.value}",
        role=role,
        is_active=True,
        is_verified=True,
    )
    session.add(u)
    await session.commit()
    await session.refresh(u)
    return u


@pytest_asyncio.fixture
async def superadmin(session) -> User:
    return await _make_user(session, "super@test.uz", Role.SUPERADMIN)


@pytest_asyncio.fixture
async def admin(session) -> User:
    return await _make_user(session, "admin@test.uz", Role.ADMIN)


@pytest_asyncio.fixture
async def content_manager(session) -> User:
    return await _make_user(session, "cm@test.uz", Role.CONTENT_MANAGER)


@pytest_asyncio.fixture
async def page_editor(session) -> User:
    return await _make_user(session, "pe@test.uz", Role.PAGE_EDITOR)


async def _login_token(client: AsyncClient, email: str, password: str = "TestPass123!") -> str:
    res = await client.post("/api/auth/login", json={"email": email, "password": password})
    assert res.status_code == 200, res.text
    return res.json()["access_token"]


@pytest_asyncio.fixture
async def auth_headers_super(client, superadmin) -> dict:
    token = await _login_token(client, superadmin.email)
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def auth_headers_admin(client, admin) -> dict:
    token = await _login_token(client, admin.email)
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def auth_headers_cm(client, content_manager) -> dict:
    token = await _login_token(client, content_manager.email)
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def auth_headers_pe(client, page_editor) -> dict:
    token = await _login_token(client, page_editor.email)
    return {"Authorization": f"Bearer {token}"}


# ===== Content fixtures =====

@pytest_asyncio.fixture
async def sample_category(session) -> NewsCategory:
    c = NewsCategory(slug="test-cat", name_uz="Test", name_ru="Тест", name_en="Test")
    session.add(c)
    await session.commit()
    await session.refresh(c)
    return c


@pytest_asyncio.fixture
async def sample_news(session, sample_category, admin) -> News:
    n = News(
        slug="sample-post",
        title_uz="Sarlavha", title_ru="Заголовок", title_en="Title",
        excerpt_uz="qisqa", excerpt_ru="кратко", excerpt_en="short",
        body_uz="matn", body_ru="текст", body_en="text",
        is_published=True,
        category_id=sample_category.id,
        author_id=admin.id,
    )
    session.add(n)
    await session.commit()
    await session.refresh(n)
    return n


@pytest_asyncio.fixture
async def sample_page(session, admin) -> StaticPage:
    p = StaticPage(
        slug="about",
        title_uz="Biz haqimizda", title_ru="О нас", title_en="About",
        content_uz="<p>uz</p>", content_ru="<p>ru</p>", content_en="<p>en</p>",
        is_published=True,
        created_by=admin.id,
    )
    session.add(p)
    await session.commit()
    await session.refresh(p)
    return p
