"""Application‑wide settings."""
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/maframework"
    ollama_host: str = "http://localhost:11434"
    default_llm: str = "llama3:8b"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
