from datetime import datetime
from pydantic import BaseModel, ConfigDict


class LeaderBase(BaseModel):
    enabled: bool = True
    sort_order: int = 0
    group: str  # rector | prorector | dean | department_head
    name_uz: str
    name_ru: str
    name_en: str
    position_uz: str = ""
    position_ru: str = ""
    position_en: str = ""
    degree_uz: str = ""
    degree_ru: str = ""
    degree_en: str = ""
    bio_uz: str = ""
    bio_ru: str = ""
    bio_en: str = ""
    photo: str | None = None
    email: str | None = None
    phone: str | None = None


class LeaderCreate(LeaderBase):
    pass


class LeaderUpdate(BaseModel):
    enabled: bool | None = None
    sort_order: int | None = None
    group: str | None = None
    name_uz: str | None = None
    name_ru: str | None = None
    name_en: str | None = None
    position_uz: str | None = None
    position_ru: str | None = None
    position_en: str | None = None
    degree_uz: str | None = None
    degree_ru: str | None = None
    degree_en: str | None = None
    bio_uz: str | None = None
    bio_ru: str | None = None
    bio_en: str | None = None
    photo: str | None = None
    email: str | None = None
    phone: str | None = None


class LeaderAdminOut(LeaderBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime


class LeaderPublicOut(BaseModel):
    id: int
    group: str
    name: str
    position: str
    degree: str
    bio: str
    photo: str | None
    email: str | None
    phone: str | None
