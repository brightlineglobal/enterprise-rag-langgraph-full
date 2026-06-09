#!/usr/bin/env bash
set -e
PROJECT_ID="${PROJECT_ID:-your-gcp-project-id}"
REGION="${REGION:-us-central1}"
REPOSITORY="${REPOSITORY:-enterprise-rag-repo}"
IMAGE_NAME="${IMAGE_NAME:-rag-api}"
TAG="${TAG:-latest}"
IMAGE_URI="$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/$IMAGE_NAME:$TAG"
docker build -t "$IMAGE_URI" .
docker push "$IMAGE_URI"
echo "Pushed: $IMAGE_URI"
