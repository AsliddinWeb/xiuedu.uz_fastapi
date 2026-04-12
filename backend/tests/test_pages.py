import pytest

pytestmark = pytest.mark.asyncio


async def test_get_page_by_slug_published(client, sample_page):
    res = await client.get(f"/api/pages/{sample_page.slug}?lang=ru")
    assert res.status_code == 200
    body = res.json()
    assert body["slug"] == sample_page.slug
    # ru localization
    assert "ru" in body["content"]


async def test_get_page_draft_forbidden_public(client, session, sample_page):
    sample_page.is_published = False
    await session.commit()
    res = await client.get(f"/api/pages/{sample_page.slug}")
    assert res.status_code == 404


async def test_create_page_as_page_editor(client, auth_headers_pe):
    res = await client.post(
        "/api/admin/pages/",
        json={
            "slug": "rules",
            "title_uz": "Qoidalar", "title_ru": "Правила", "title_en": "Rules",
            "content_uz": "<p>q</p>", "content_ru": "<p>r</p>", "content_en": "<p>e</p>",
        },
        headers=auth_headers_pe,
    )
    assert res.status_code == 201


async def test_create_page_as_content_manager_forbidden(client, auth_headers_cm):
    res = await client.post(
        "/api/admin/pages/",
        json={"slug": "x", "title_uz": "x", "title_ru": "x", "title_en": "x"},
        headers=auth_headers_cm,
    )
    assert res.status_code == 403


async def test_delete_page_admin(client, sample_page, auth_headers_admin):
    res = await client.delete(f"/api/admin/pages/{sample_page.id}", headers=auth_headers_admin)
    assert res.status_code == 204


async def test_list_pages_public(client, sample_page):
    res = await client.get("/api/pages/")
    assert res.status_code == 200
    assert any(p["slug"] == sample_page.slug for p in res.json())
