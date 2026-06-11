from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GROQ_API_KEY: str
    PINECONE_API_KEY: str
    PINECONE_INDEX_NAME: str = "erp-compliance"
    DATABASE_URL: str = "sqlite+aiosqlite:///./erp_enterprise.db"
    ENV: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()