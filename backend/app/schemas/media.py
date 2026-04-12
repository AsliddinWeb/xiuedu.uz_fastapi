import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MediaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    original_name: str
    mime_type: str
    size_bytes: int
    url: str
    width: int | None
    height: int | None
    alt_uz: str | None
    alt_ru: str | None
    alt_en: str | None
    uploaded_by: uuid.UUID | None
    created_at: datetime


class MediaUploadResponse(BaseModel):
    id: int
    url: str
    thumbnail_url: str | None
    medium_url: str | None
    filename: str
    size_bytes: int
    mime_type: str
    width: int | None
    height: int | None


class MediaAltUpdate(BaseModel):
    alt_uz: str | None = None
    alt_ru: str | None = None
    alt_en: str | None = None
