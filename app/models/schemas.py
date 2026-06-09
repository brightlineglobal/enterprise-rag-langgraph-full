from typing import Any
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    question: str = Field(..., min_length=2)
    user_id: str | None = None
    department: str | None = None
    access_groups: list[str] = Field(default_factory=list)

class SourceDocument(BaseModel):
    id: int
    source_file: str
    title: str | None = None
    chunk_text: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    similarity: float | None = None
    rerank_score: float | None = None

class ChatResponse(BaseModel):
    question: str
    rewritten_question: str
    answer: str
    sources: list[SourceDocument]

class FeedbackRequest(BaseModel):
    question: str
    answer: str
    rating: int | None = Field(default=None, ge=1, le=5)
    comment: str | None = None
    user_id: str | None = None

class IngestResponse(BaseModel):
    message: str
    files_processed: int
    chunks_inserted: int
