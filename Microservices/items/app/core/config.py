from pydantic_settings import BaseSettings
from typing import List
from pydantic import AnyHttpUrl

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "change-me"  # must match AUTH service for JWT validation
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    ENVIRONMENT: str = "local"

settings = Settings()
