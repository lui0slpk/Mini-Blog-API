from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./blog.db"
    JWT_SECRET_KEY: str = "change-my-in-prod"
    JWT_ACCESS_TOKEN_EXPIRES_MINUTES: int = 30
    JWT_ALGORITHM: str = "HS256"
    MAX_UPLOAD_MB: int = 10

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
