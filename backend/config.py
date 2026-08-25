from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # ==========================================
    # APPLICATION
    # ==========================================

    APP_NAME: str = "AyurConnect"

    APP_VERSION: str = "1.0.0"

    DEBUG: bool = True

    # ==========================================
    # GEMINI
    # ==========================================

    GEMINI_API_KEY: str

    # ==========================================
    # DATABASE
    # ==========================================

    DATABASE_URL: str = (
        "sqlite:///./ayurconnection.db"
    )

    # ==========================================
    # JWT AUTHENTICATION
    # ==========================================

    JWT_SECRET_KEY: str = (
        "ayurconnect-development-secret-key"
    )

    JWT_ALGORITHM: str = "HS256"

    # ==========================================
    # ENVIRONMENT CONFIGURATION
    # ==========================================

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()