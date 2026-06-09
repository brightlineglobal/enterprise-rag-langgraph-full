#!/usr/bin/env bash
set -e
PROJECT_ID="${PROJECT_ID:-your-gcp-project-id}"
REGION="${REGION:-us-central1}"
REPOSITORY="${REPOSITORY:-enterprise-rag-repo}"
IMAGE_NAME="${IMAGE_NAME:-rag-api}"
TAG="${TAG:-latest}"
SERVICE_NAME="${SERVICE_NAME:-enterprise-rag-api}"
IMAGE_URI="$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/$IMAGE_NAME:$TAG"
gcloud run deploy "$SERVICE_NAME" --image "$IMAGE_URI" --region "$REGION" --platform managed --allow-unauthenticated --memory 1Gi --cpu 1 --set-env-vars ENVIRONMENT=prod
