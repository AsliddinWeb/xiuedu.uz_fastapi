import pytest

pytestmark = pytest.mark.asyncio


async def test_get_news_list_public(client, sample_news):
    res = await client.get("/api/news/")
    assert res.status_code == 200
    items = res.json()["items"]
    assert any(n["slug"] == sample_news.slug for n in items)


async def test_get_news_detail_increments_views(client, sample_news):
    initial = sample_news.views_count
    res = await client.get(f"/api/news/{sample_news.slug}")
    assert res.status_code == 200
    assert res.json()["views_count"] == initial + 1


async def test_create_news_as_content_manager(client, auth_headers_cm, sample_category):
    payload = {
        "slug": "new-post",
        "title_uz": "Yangi", "title_ru": "Новый", "title_en": "New",
        "category_id": sample_category.id,
        "is_published": False,
    }
    res = await client.post("/api/admin/news/", json=payload, headers=auth_headers_cm)
    assert res.status_code == 201
    assert res.json()["slug"] == "new-post"


async def test_create_news_as_page_editor_forbidden(client, auth_headers_pe):
    payload = {"slug": "x", "title_uz": "x", "title_ru": "x", "title_en": "x"}
    res = await client.post("/api/admin/news/", json=payload, headers=auth_headers_pe)
    assert res.status_code == 403


async def test_publish_unpublish_news(client, sample_news, auth_headers_admin):
    res = await client.patch(
        f"/api/admin/news/{sample_news.id}/publish?publish=false",
        headers=auth_headers_admin,
    )
    assert res.status_code == 200
    assert res.json()["is_published"] is False


async def test_delete_news(client, sample_news, auth_headers_admin):
    res = await client.delete(f"/api/admin/news/{sample_news.id}", headers=auth_headers_admin)
    assert res.status_code == 204


async def test_news_stats(client, sample_news, auth_headers_admin):
    res = await client.get("/api/admin/news/stats", headers=auth_headers_admin)
    assert res.status_code == 200
    body = res.json()
    assert body["total"] >= 1
    assert body["published"] >= 1
