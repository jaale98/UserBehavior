from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    app_env: str = "development"
    app_debug: bool = True
    app_secret_key: str = "change-me-in-prod"
    cors_origins: List[str] = []
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/userbehavior"

    jwt_algorithm: str = "HS256"
    access_token_expires_minutes: int = 60

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str) and not v.strip().startswith("["):
            return [s.strip() for s in v.split(",") if s.strip()]
        return v

    class Config:
        env_prefix = ""
        case_sensitive = False
        env_file = ".env" if os.path.exists(".env") else None

settings = Settings()