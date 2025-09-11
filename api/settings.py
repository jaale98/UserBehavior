from pydantic import BaseModel, AnyHttpUrl
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    app_env: str = "development"
    app_debug: bool = True
    app_secret_key: str = "change-me-in-prod"
    cors_origins: List[AnyHttpUrl] = []
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/userbehavior"

    class Config:
        env_prefix = ""
        case_sensitive = False
        env_file = ".env" if os.path.exists(".env") else None

settings = Settings()