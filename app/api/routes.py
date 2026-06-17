from fastapi import APIRouter
from google.genai.errors import APIError
from app.core.config import settings
from app.models.schemas import ChatRequest, ChatResponse, FeedbackRequest, IngestResponse
from app.rag.graph import rag_graph
from app.services.db_service import count_documents, insert_feedback
from app.services.ingestion_service import ingest_from_gcs

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/stats")
def stats():
    return {"documents": count_documents()}

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if not settings.gemini_api_key.strip() or settings.gemini_api_key == "replace_with_your_gemini_api_key":
        return {
            "question": request.question,
            "rewritten_question": request.question,
            "answer": "I am still working on it... Please wait till Gemini agree to work with me :-)",
            "sources": [],
        }

    try:
        result = rag_graph.invoke({
            "question": request.question,
            "user_id": request.user_id,
            "department": request.department,
            "access_groups": request.access_groups,
            "rewritten_question": "",
            "retrieved_docs": [],
            "reranked_docs": [],
            "answer": "",
        })
    except APIError as exc:
        return {
            "question": request.question,
            "rewritten_question": request.question,
            "answer": f"Gemini is not ready to answer yet: {exc}",
            "sources": [],
        }

    return {"question": request.question, "rewritten_question": result["rewritten_question"], "answer": result["answer"], "sources": result["reranked_docs"]}

@router.post("/ingest/gcs", response_model=IngestResponse)
def ingest_gcs():
    files_processed, chunks_inserted = ingest_from_gcs()
    return {"message": "GCS ingestion completed", "files_processed": files_processed, "chunks_inserted": chunks_inserted}

@router.post("/feedback")
def feedback(request: FeedbackRequest):
    insert_feedback(request.question, request.answer, request.rating, request.comment, request.user_id)
    return {"message": "Feedback saved"}
