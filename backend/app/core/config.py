from functools import lru_cache
from typing import Literal
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[3]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", case_sensitive=False, extra="ignore")

    # ── App ───────────────────────────────────────────────────────────────────
    APP_ENV: Literal["development", "production", "test"] = "development"
    SECRET_KEY: str
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_origins(cls, v: str | list) -> list[str]:
        if isinstance(v, str):
            return [o.strip() for o in v.split(",")]
        return v

    # ── Database ──────────────────────────────────────────────────────────────
    DATABASE_URL: str
    POSTGRES_USER: str = "my_portfolio"
    POSTGRES_PASSWORD: str = "abhishek"
    POSTGRES_DB: str = "portfolio"

    # ── Redis ─────────────────────────────────────────────────────────────────
    REDIS_URL: str = "redis://redis:6379/0"
    CELERY_BROKER_URL: str = "redis://redis:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/2"

    # ── OpenAI ────────────────────────────────────────────────────────────────
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o"
    AI_SYSTEM_PROMPT: str = "You are an AI assistant for a software developer portfolio."

    # ── GitHub ────────────────────────────────────────────────────────────────
    GITHUB_TOKEN: str = ""
    GITHUB_USERNAME: str = ""

    # ── Email ─────────────────────────────────────────────────────────────────
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = ""
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_TO: str = ""

    # ── AWS ───────────────────────────────────────────────────────────────────
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_S3_BUCKET: str = "portfolio-assets"
    AWS_REGION: str = "us-east-1"

    # ── Admin ─────────────────────────────────────────────────────────────────
    ADMIN_EMAIL: str = "admin@example.com"
    ADMIN_PASSWORD: str = "changeme"

    # ── Sentry ────────────────────────────────────────────────────────────────
    SENTRY_DSN: str = ""

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()