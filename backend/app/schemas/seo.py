from pydantic import BaseModel, ConfigDict


class GlobalSEOItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    key: str
    value: str
    description: str | None


class GlobalSEOUpdate(BaseModel):
    value: str
    description: str | None = None


class RedirectBase(BaseModel):
    old_path: str
    new_path: str
    status_code: int = 301
    is_active: bool = True


class RedirectCreate(RedirectBase):
    pass


class RedirectUpdate(BaseModel):
    old_path: str | None = None
    new_path: str | None = None
    status_code: int | None = None
    is_active: bool | None = None


class RedirectOut(RedirectBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
