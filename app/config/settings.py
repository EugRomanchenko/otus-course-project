from typing import Any, Dict, Optional
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, field_validator
from os import getenv


class Settings(BaseSettings):

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Optional[str]) -> str:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=getenv("POSTGRES_USER", "postgres"),
            password=getenv("POSTGRES_PASSWORD"),
            host=getenv("POSTGRES_SERVER"),
            path=f"{getenv('POSTGRES_DB') or ''}",
        ).unicode_string()


settings = Settings()
