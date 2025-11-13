# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./app/tickets.db"
    ENV: str = "dev"
    AZURE_ENDPOINT: str = ""
    AZURE_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
