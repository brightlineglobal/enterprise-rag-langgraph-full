# Enterprise RAG Searchbot with LangGraph, FastAPI, PostgreSQL/pgvector, GCS, Gemini, and Reranking

VS Code-ready starter implementation for an Enterprise Knowledge Base RAG Searchbot.

## Architecture

User -> FastAPI /chat -> LangGraph workflow -> query rewrite -> Gemini embedding -> PostgreSQL + pgvector retrieval -> reranking -> Gemini answer generation -> answer + citations.

## Included

- FastAPI application
- LangGraph RAG workflow
- PostgreSQL with pgvector
- Google Cloud Storage ingestion
- Gemini embedding integration
- Gemini answer generation
- Simple lexical + vector reranker
- Docker Compose with two containers
- GCP Artifact Registry and Cloud Run scripts
- SQL initialization
- Tests
- Environment examples

## Local setup

```bash
cp .env.example .env
docker compose up --build
```

Health check:

```bash
curl http://localhost:8000/health
```

Ingest from GCS:

```bash
curl -X POST http://localhost:8000/ingest/gcs
```

Ask a question:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"How do I request VPN access?","user_id":"gilman","department":"IT"}'
```

## Production notes

For production, prefer Cloud SQL for PostgreSQL instead of running the database as a container. Use Secret Manager for GEMINI_API_KEY and database credentials.
