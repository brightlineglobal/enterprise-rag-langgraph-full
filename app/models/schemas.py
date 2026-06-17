from typing import Any, Optional
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    question: str = Field(..., min_length=2)
    user_id: Optional[str] = None
    department: Optional[str] = None
    access_groups: list[str] = Field(default_factory=list)

class SourceDocument(BaseModel):
    id: int
    source_file: str
    title: Optional[str] = None
    chunk_text: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    similarity: Optional[float] = None
    rerank_score: Optional[float] = None

class ChatResponse(BaseModel):
    question: str
    rewritten_question: str
    answer: str
    sources: list[SourceDocument]

class FeedbackRequest(BaseModel):
    question: str
    answer: str
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    comment: Optional[str] = None
    user_id: Optional[str] = None

class IngestResponse(BaseModel):
    message: str
    files_processed: int
    chunks_inserted: int
