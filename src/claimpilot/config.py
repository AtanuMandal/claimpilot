"""Typed application settings, loaded from environment variables and the .env file."""

from enum import StrEnum
from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    LOCAL = "local"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """All configuration in one typed object.

    Each field is read from the environment variable with the same name
    (case-insensitive): app_env <- APP_ENV, google_api_key <- GOOGLE_API_KEY.
    Real environment variables take priority over values in .env.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: Environment = Environment.LOCAL
    google_api_key: SecretStr
    llm_model: str = "gemini-3.5-flash-lite"


@lru_cache
def get_settings() -> Settings:
    """Create the settings once and reuse them everywhere."""
    return Settings()  # type: ignore[call-arg]  # values come from the environment