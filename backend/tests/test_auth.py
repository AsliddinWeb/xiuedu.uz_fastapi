import pytest

pytestmark = pytest.mark.asyncio


async def test_login_success(client, admin):
    res = await client.post("/api/auth/login", json={"email": admin.email, "password": "TestPass123!"})
    assert res.status_code == 200
    body = res.json()
    assert body["access_token"]
    assert body["refresh_token"]
    assert body["user"]["email"] == admin.email
    assert body["user"]["role"] == "admin"


async def test_login_wrong_password(client, admin):
    res = await client.post("/api/auth/login", json={"email": admin.email, "password": "WRONG"})
    assert res.status_code == 401


async def test_login_inactive_user(client, session, admin):
    admin.is_active = False
    await session.commit()
    res = await client.post("/api/auth/login", json={"email": admin.email, "password": "TestPass123!"})
    assert res.status_code == 403


async def test_get_me_unauthorized(client):
    res = await client.get("/api/auth/me")
    assert res.status_code == 401


async def test_get_me_authorized(client, auth_headers_admin):
    res = await client.get("/api/auth/me", headers=auth_headers_admin)
    assert res.status_code == 200
    assert res.json()["role"] == "admin"


async def test_refresh_token(client, admin):
    login = await client.post("/api/auth/login", json={"email": admin.email, "password": "TestPass123!"})
    refresh = login.json()["refresh_token"]
    res = await client.post("/api/auth/refresh", json={"refresh_token": refresh})
    assert res.status_code == 200
    assert res.json()["access_token"]


async def test_logout(client, auth_headers_admin):
    res = await client.post("/api/auth/logout", headers=auth_headers_admin)
    assert res.status_code == 204
