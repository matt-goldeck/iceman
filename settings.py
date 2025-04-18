from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_nested_delimiter="__"
    )

    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    ORIGINS: list[str] = ["*"]


settings = Settings()
