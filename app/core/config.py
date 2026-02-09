from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    # APP
    app_name: str
    app_prefix: str

    # API
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str

    # SECURITY
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # CORS
    backend_cors_origins: List[str] = []

    class Config:
        env_file = ".env"


settings = Settings()
