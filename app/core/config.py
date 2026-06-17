from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Enterprise RAG Searchbot"
    environment: str = "local"
    database_url: str
    gemini_api_key: str
    gemini_embedding_model: str = "gemini-embedding-001"
    gemini_generation_model: str = "gemini-2.5-flash"
    gemini_temperature: float = 0.0
    gcs_bucket_name: str
    google_application_credentials: Optional[str] = None
    retrieval_limit: int = 20
    rerank_limit: int = 5
    chunk_size: int = 1000
    chunk_overlap: int = 150
    embedding_dimension: int = 768
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
