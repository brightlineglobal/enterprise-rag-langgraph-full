from fastapi import APIRouter
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
    return {"question": request.question, "rewritten_question": result["rewritten_question"], "answer": result["answer"], "sources": result["reranked_docs"]}

@router.post("/ingest/gcs", response_model=IngestResponse)
def ingest_gcs():
    files_processed, chunks_inserted = ingest_from_gcs()
    return {"message": "GCS ingestion completed", "files_processed": files_processed, "chunks_inserted": chunks_inserted}

@router.post("/feedback")
def feedback(request: FeedbackRequest):
    insert_feedback(request.question, request.answer, request.rating, request.comment, request.user_id)
    return {"message": "Feedback saved"}
