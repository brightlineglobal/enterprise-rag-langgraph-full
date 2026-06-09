from app.core.config import settings
from app.services.chunking import chunk_text
from app.services.db_service import insert_document
from app.services.gcs_service import load_documents_from_gcs
from app.services.gemini_service import gemini_service

def ingest_from_gcs() -> tuple[int, int]:
    documents = load_documents_from_gcs()
    chunks_inserted = 0
    for doc in documents:
        chunks = chunk_text(doc["content"], settings.chunk_size, settings.chunk_overlap)
        for index, chunk in enumerate(chunks):
            embedding = gemini_service.embed_text(chunk)
            metadata = {**doc["metadata"], "chunk_index": index, "access_groups": []}
            insert_document(doc["source_file"], doc["title"], chunk, metadata, embedding)
            chunks_inserted += 1
    return len(documents), chunks_inserted
