#!/usr/bin/env bash
set -e
PROJECT_ID="${PROJECT_ID:-your-gcp-project-id}"
REGION="${REGION:-us-central1}"
REPOSITORY="${REPOSITORY:-enterprise-rag-repo}"
gcloud config set project "$PROJECT_ID"
gcloud artifacts repositories create "$REPOSITORY" --repository-format=docker --location="$REGION" --description="Enterprise RAG container repository" || true
gcloud auth configure-docker "$REGION-docker.pkg.dev"
