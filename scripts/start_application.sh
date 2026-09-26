#!/bin/bash

set -e

DOCKER_IMAGE="pavanpilla/ann-project:latest"

echo "Pulling Docker image..."

docker pull "$DOCKER_IMAGE"

echo "Starting ANN application..."

docker run -d \
  --name ann-project \
  -p 8501:8501 \
  "$DOCKER_IMAGE"

echo "ANN application started successfully."