# scripts/install.sh
# Скрипт для встановлення та запуску платформи HoloMisha RealityForge

#!/bin/bash
set -e

echo "Setting up HoloMisha RealityForge..."

# Install dependencies
pip install --no-cache-dir -r config/requirements.txt

# Initialize database
python config/init_database.py

# Build Docker images
docker build -t gcr.io/holomisha-project/holomisha:latest .
docker build -f Dockerfile.webxr -t gcr.io/holomisha-project/webxr:latest .

# Push to Google Container Registry
gcloud auth configure-docker
docker push gcr.io/holomisha-project/holomisha:latest
docker push gcr.io/holomisha-project/webxr:latest

# Start services
docker-compose -f docker-compose.yml up -d

# Apply Kubernetes configuration
kubectl apply -f kubernetes.yaml

echo "HoloMisha RealityForge deployed successfully! 🌌"