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

From a fresh clone, the app can be started with Docker Compose:

```bash
git pull
docker compose up --build
```

The repository includes a sanitized `.env` file so Compose can start immediately. To enable real Gemini answers, set your local key in `.env`:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Then restart the API:

```bash
docker compose up -d --build
```

If port `8000` is already in use, choose another host port:

```bash
API_PORT=8001 docker compose up -d --build
```

On a fresh database volume, Docker runs all SQL files in `sql/` automatically:

- `sql/init.sql`
- `sql/sample_test_data.sql`

The chat UI is available at:

```bash
http://localhost:8000/
```

Health check:

```bash
curl http://localhost:8000/health
```

Load or refresh sample test data on an existing database volume:

```bash
docker compose exec -T db psql -U raguser -d ragdb < sql/sample_test_data.sql
```

Restore the committed database snapshot instead:

```bash
docker compose exec -T db psql -U raguser -d ragdb < deployment/database/ragdb_dump.sql
```

Ingest from GCS:

```bash
curl -X POST http://localhost:8000/ingest/gcs
```

GCS ingestion is optional. To use it locally, provide Google credentials and set `GOOGLE_APPLICATION_CREDENTIALS` to the credentials path available inside the API container.

Ask a question:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"How do I request VPN access?","user_id":"gilman","department":"IT"}'
```

## Production notes

For production, prefer Cloud SQL for PostgreSQL instead of running the database as a container. Use Secret Manager for GEMINI_API_KEY and database credentials.
