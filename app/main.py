from fastapi import FastAPI
from app.api.routes import router
from app.core.config import settings
from app.core.logging import configure_logging

configure_logging()

app = FastAPI(
    title=settings.app_name,
    description="Enterprise Knowledge Base RAG Searchbot using LangGraph, FastAPI, pgvector, GCS, and Gemini.",
    version="1.0.0",
)
app.include_router(router)
