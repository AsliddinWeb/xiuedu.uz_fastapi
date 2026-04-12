from functools import lru_cache
from typing import List

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # ===== Database =====
    DATABASE_URL: str = (
        "postgresql+asyncpg://xiuedu:xiuedu_secret@db:5432/xiuedu"
    )

    # ===== Redis =====
    REDIS_URL: str = "redis://redis:6379/0"

    # ===== JWT / Security =====
    SECRET_KEY: str = "change-me-please"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ===== CORS (comma-separated string) =====
    ALLOWED_ORIGINS: str = "http://localhost,http://localhost:5176"

    @computed_field
    @property
    def cors_origins(self) -> List[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",") if o.strip()]

    # ===== Site / Uploads =====
    SITE_URL: str = "https://xiuedu.uz"
    SITE_NAME: str = "Xalqaro Innovatsion Universiteti"
    UPLOAD_DIR: str = "/app/media"
    MAX_UPLOAD_SIZE_MB: int = 20

    # ===== Rate limit =====
    RATE_LIMIT_DEFAULT: str = "200/minute"
    RATE_LIMIT_AUTH: str = "10/minute"

    # ===== Admin bootstrap =====
    ADMIN_EMAIL: str = "admin@xiuedu.uz"
    ADMIN_PASSWORD: str = "ChangeMe123!"

    # ===== AI Chat (Groq) =====
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # ===== Environment =====
    ENV: str = "development"
    DEBUG: bool = True


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
