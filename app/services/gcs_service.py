import json
import logging
from typing import Any
from google.cloud import storage
from app.core.config import settings

logger = logging.getLogger(__name__)
SUPPORTED_EXTENSIONS = (".txt", ".md", ".csv", ".json")

def load_documents_from_gcs() -> list[dict[str, Any]]:
    client = storage.Client()
    bucket = client.bucket(settings.gcs_bucket_name)
    docs: list[dict[str, Any]] = []
    for blob in bucket.list_blobs():
        if not blob.name.lower().endswith(SUPPORTED_EXTENSIONS):
            logger.info("Skipping unsupported file: %s", blob.name)
            continue
        raw_text = blob.download_as_text()
        if blob.name.lower().endswith(".json"):
            try:
                raw_text = json.dumps(json.loads(raw_text), indent=2)
            except Exception:
                pass
        docs.append({
            "source_file": blob.name,
            "title": blob.name.split("/")[-1],
            "content": raw_text,
            "metadata": {
                "bucket": settings.gcs_bucket_name,
                "gcs_path": blob.name,
                "generation": blob.generation,
                "updated": blob.updated.isoformat() if blob.updated else None,
                "content_type": blob.content_type,
            },
        })
    return docs
