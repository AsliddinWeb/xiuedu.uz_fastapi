import io

import pytest
from PIL import Image

pytestmark = pytest.mark.asyncio


def _png_bytes(size=(100, 100)) -> bytes:
    img = Image.new("RGB", size, color=(180, 60, 60))
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return buf.getvalue()


async def test_upload_image_success(client, auth_headers_admin, tmp_path, monkeypatch):
    from app.config import settings
    monkeypatch.setattr(settings, "UPLOAD_DIR", str(tmp_path))

    files = {"file": ("test.png", _png_bytes(), "image/png")}
    res = await client.post("/api/admin/media/upload", files=files, headers=auth_headers_admin)
    assert res.status_code == 201
    body = res.json()
    assert body["url"].startswith("/media/")
    assert body["thumbnail_url"]
    assert body["medium_url"]


async def test_upload_oversized_rejected(client, auth_headers_admin):
    big = b"x" * (11 * 1024 * 1024)  # 11MB > 10MB image limit
    files = {"file": ("big.png", big, "image/png")}
    res = await client.post("/api/admin/media/upload", files=files, headers=auth_headers_admin)
    assert res.status_code == 413


async def test_upload_invalid_type_rejected(client, auth_headers_admin):
    files = {"file": ("script.exe", b"MZ\x00\x00", "application/x-msdownload")}
    res = await client.post("/api/admin/media/upload", files=files, headers=auth_headers_admin)
    assert res.status_code == 415


async def test_upload_unauthenticated(client):
    files = {"file": ("test.png", _png_bytes(), "image/png")}
    res = await client.post("/api/admin/media/upload", files=files)
    assert res.status_code == 401
