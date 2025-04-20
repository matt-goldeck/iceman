from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Load from .env.local
load_dotenv(dotenv_path=".env.local")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_nested_delimiter="__"
    )

    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    ORIGINS: list[str] = ["*"]

    OPEN_AI_API_KEY: str

    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    # TODO: Migrate to SQLAlchemy
    SUPABASE_URL: str
    SUPABASE_SERVICE_KEY: str


settings = Settings()
