from pathlib import Path
from pydantic_settings import BaseSettings
from functools import lru_cache

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    database_url: str = "sqlite:///./orbitz.db"
    secret_key: str = "orbitz-dev-secret-change-in-production"
    access_token_expire_minutes: int = 60 * 24 * 7
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    algorithm: str = "HS256"

    class Config:
        env_file = str(BASE_DIR / ".env")
        extra = "ignore"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
