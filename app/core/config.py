from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GROQ_API_KEY: str
    GROQ_MODEL: str
    DATABASE_URL: str
    LOG_LEVEL: str
    LOG_TO_FILE: bool
    LOG_FILE: str
    LOG_MAX_BYTES: int
    LOG_BACKUP_COUNT: int
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
