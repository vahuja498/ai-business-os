from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    DATABASE_URL: str = "sqlite+aiosqlite:///./ai_business_os.db"

    # Model Provider Configuration
    MODEL_PROVIDER: str = "mock"
    MODEL_NAME: str | None = None
    OPENAI_API_KEY: str | None = None
    GEMINI_API_KEY: str | None = None
    ANTHROPIC_API_KEY: str | None = None

    # Financial Guardrails
    MAX_DAILY_SPEND: float = 500.0
    MAX_TRANSACTION_AMOUNT: float = 1000.0
    MAX_MONTHLY_SPEND: float = 10000.0
    MIN_MARGIN: float = 0.20
    MIN_CASH_RESERVE: float = 5000.0


settings = Settings()
