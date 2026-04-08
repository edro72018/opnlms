from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "OpenLMS"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    DATABASE_URL: str = "sqlite+aiosqlite:///./opnlms.db"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
