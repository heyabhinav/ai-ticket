# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./app/tickets.db"

    # Azure OpenAI (gpt-5-nano) config
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_KEY: str
    AZURE_OPENAI_DEPLOYMENT: str
    AZURE_OPENAI_API_VERSION: str = "2024-10-21"

    class Config:
        env_file = ".env"

settings = Settings()
