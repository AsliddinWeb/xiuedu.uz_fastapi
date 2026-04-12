import os
import uuid
from datetime import datetime
from io import BytesIO
from pathlib import Path

from fastapi import HTTPException, UploadFile
from PIL import Image

from app.config import settings

IMAGE_MIMES = {"image/jpeg", "image/jpg", "image/png", "image/webp", "image/gif"}
DOC_MIMES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}

MAX_IMAGE_BYTES = 10 * 1024 * 1024
MAX_DOC_BYTES = 50 * 1024 * 1024

THUMB_SIZE = (300, 200)
MEDIUM_SIZE = (800, 600)


def _date_subdir() -> str:
    now = datetime.utcnow()
    return f"uploads/{now.year:04d}/{now.month:02d}"


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


async def process_upload(file: UploadFile) -> dict:
    """Validate, save and (if image) generate thumb + medium webp variants.

    Returns dict suitable for MediaFile creation:
        { kind, filename, original_name, mime_type, size_bytes, url,
          thumbnail_url, medium_url, width, height }
    """
    mime = (file.content_type or "").lower()
    is_image = mime in IMAGE_MIMES
    is_doc = mime in DOC_MIMES
    if not (is_image or is_doc):
        raise HTTPException(415, f"Unsupported media type: {mime}")

    raw = await file.read()
    size = len(raw)
    if is_image and size > MAX_IMAGE_BYTES:
        raise HTTPException(413, "Image exceeds 10MB limit")
    if is_doc and size > MAX_DOC_BYTES:
        raise HTTPException(413, "Document exceeds 50MB limit")

    sub = _date_subdir()
    base_dir = Path(settings.UPLOAD_DIR) / sub
    _ensure_dir(base_dir)

    uid = uuid.uuid4().hex
    ext = os.path.splitext(file.filename or "")[1].lower() or ""

    width: int | None = None
    height: int | None = None
    thumbnail_url: str | None = None
    medium_url: str | None = None

    if is_image:
        # Convert original to webp (smaller)
        img = Image.open(BytesIO(raw))
        if img.mode in ("P", "RGBA"):
            img = img.convert("RGBA") if "A" in img.mode else img.convert("RGB")
        else:
            img = img.convert("RGB")
        width, height = img.size

        filename = f"{uid}.webp"
        original_path = base_dir / filename
        img.save(original_path, "WEBP", quality=85, method=6)

        # thumbnail
        thumb = img.copy()
        thumb.thumbnail(THUMB_SIZE)
        thumb_name = f"{uid}_thumb.webp"
        thumb.save(base_dir / thumb_name, "WEBP", quality=80, method=6)

        # medium
        medium = img.copy()
        medium.thumbnail(MEDIUM_SIZE)
        medium_name = f"{uid}_md.webp"
        medium.save(base_dir / medium_name, "WEBP", quality=82, method=6)

        url = f"/media/{sub}/{filename}"
        thumbnail_url = f"/media/{sub}/{thumb_name}"
        medium_url = f"/media/{sub}/{medium_name}"
        kind = "image"
        actual_size = original_path.stat().st_size
    else:
        filename = f"{uid}{ext}"
        path = base_dir / filename
        path.write_bytes(raw)
        url = f"/media/{sub}/{filename}"
        kind = "document"
        actual_size = size

    return {
        "kind": kind,
        "filename": filename,
        "original_name": file.filename or filename,
        "mime_type": mime,
        "size_bytes": actual_size,
        "url": url,
        "thumbnail_url": thumbnail_url,
        "medium_url": medium_url,
        "width": width,
        "height": height,
    }


def delete_file(url: str) -> None:
    """Best-effort delete of a /media/* URL and its variants."""
    if not url.startswith("/media/"):
        return
    rel = url[len("/media/"):]
    base = Path(settings.UPLOAD_DIR) / rel
    for p in (base, base.with_name(base.stem + "_thumb" + base.suffix),
              base.with_name(base.stem + "_md" + base.suffix)):
        try:
            p.unlink(missing_ok=True)
        except OSError:
            pass
