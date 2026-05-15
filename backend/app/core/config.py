"""
PRYSM Unified Configuration
==============================
Single source of truth for all application settings.
Environment-driven, typed, no hardcoded secrets.
"""

from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BACKEND_DIR / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ──────────────────────────────────────────────────────
    app_name: str = Field(default="prysm-backend", validation_alias=AliasChoices("APP_NAME", "app_name"))
    environment: str = Field(default="development", validation_alias=AliasChoices("ENV", "ENVIRONMENT", "APP_ENV", "environment"))
    debug: bool = False
    log_level: str = "INFO"

    # ── Server ───────────────────────────────────────────────────────────
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # ── Database ─────────────────────────────────────────────────────────
    database_url: str = Field(
        default=f"sqlite:///{(BACKEND_DIR / 'storage' / 'prysm.db').as_posix()}",
        validation_alias=AliasChoices("DATABASE_URL", "database_url"),
    )

    # ── Storage ──────────────────────────────────────────────────────────
    upload_dir: Path = Field(
        default=BACKEND_DIR / "storage" / "uploads",
        validation_alias=AliasChoices("UPLOAD_DIR", "upload_dir"),
    )
    chroma_persist_dir: Path = Field(
        default=BACKEND_DIR / "storage" / "chroma",
        validation_alias=AliasChoices("CHROMA_PERSIST_DIR", "chroma_persist_dir"),
    )
    report_dir: Path = Field(
        default=BACKEND_DIR / "storage" / "reports",
        validation_alias=AliasChoices("REPORT_DIR", "report_dir"),
    )
    max_upload_size_mb: int = 25

    # ── AI / LLM ─────────────────────────────────────────────────────────
    groq_api_key: str = Field(default="", validation_alias=AliasChoices("GROQ_API_KEY", "groq_api_key"))
    groq_model: str = Field(default="llama-3.3-70b-versatile", validation_alias=AliasChoices("LLM_MODEL", "groq_model"))
    llm_temperature: float = 0.1
    llm_max_tokens: int = 4096

    # ── OCR ───────────────────────────────────────────────────────────────
    tesseract_cmd: str = Field(default="", validation_alias=AliasChoices("TESSERACT_CMD", "tesseract_cmd"))

    # ── Security ──────────────────────────────────────────────────────────
    secret_key: str = Field(default="change-me-in-production", validation_alias=AliasChoices("SECRET_KEY", "secret_key"))
    access_token_expire_minutes: int = 60

    # ── Locale ────────────────────────────────────────────────────────────
    default_currency: str = "INR"

    # ── Validators ────────────────────────────────────────────────────────

    @field_validator("upload_dir", "chroma_persist_dir", "report_dir", mode="before")
    @classmethod
    def resolve_paths(cls, value: str | Path) -> Path:
        path = Path(value)
        return path if path.is_absolute() else (BACKEND_DIR / path).resolve()

    @field_validator("debug", mode="before")
    @classmethod
    def normalize_debug(cls, value: object) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"1", "true", "yes", "on", "debug"}:
                return True
            if normalized in {"0", "false", "no", "off", "release", "prod", "production"}:
                return False
        return bool(value)

    @field_validator("cors_origins", mode="before")
    @classmethod
    def normalize_cors_origins(cls, value: object) -> list[str]:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        return ["http://localhost:3000", "http://127.0.0.1:3000"]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
