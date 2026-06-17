from __future__ import annotations

import json
from typing import Any
import psycopg2
from pgvector.psycopg2 import register_vector
from app.core.config import settings

def get_connection():
    conn = psycopg2.connect(settings.database_url)
    register_vector(conn)
    return conn

def insert_document(source_file: str, title: str | None, chunk_text: str, metadata: dict[str, Any], embedding: list[float]) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO documents (source_file, title, chunk_text, metadata, embedding)
                VALUES (%s, %s, %s, %s::jsonb, %s)
            """, (source_file, title, chunk_text, json.dumps(metadata), embedding))

def search_documents(query_embedding: list[float], limit: int, access_groups: list[str] | None = None) -> list[dict[str, Any]]:
    access_groups = access_groups or []
    permission_filter = ""
    params: list[Any] = [query_embedding]
    if access_groups:
        permission_filter = """
        WHERE metadata->'access_groups' IS NULL
           OR metadata->'access_groups' = '[]'::jsonb
           OR metadata->'access_groups' ?| %s::text[]
        """
        params.append(access_groups)
    params.append(query_embedding)
    params.append(limit)
    sql = f"""
        SELECT id, source_file, title, chunk_text, metadata,
               1 - (embedding <=> %s::vector) AS similarity
        FROM documents
        {permission_filter}
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SET LOCAL ivfflat.probes = 100")
            cur.execute(sql, params)
            rows = cur.fetchall()
    return [{"id": r[0], "source_file": r[1], "title": r[2], "chunk_text": r[3], "metadata": r[4], "similarity": float(r[5]) if r[5] is not None else None} for r in rows]

def insert_feedback(question: str, answer: str, rating: int | None, comment: str | None, user_id: str | None) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO feedback (question, answer, rating, comment, user_id) VALUES (%s, %s, %s, %s, %s)", (question, answer, rating, comment, user_id))

def count_documents() -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM documents")
            return int(cur.fetchone()[0])
