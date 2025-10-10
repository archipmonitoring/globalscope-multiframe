# scripts/deploy.sh
# Скрипт для автоматизованого розгортання на production-сервері

#!/bin/bash
set -e

echo "Deploying HoloMisha RealityForge to production..."

# Build and push images
docker build -t gcr.io/holomisha-project/holomisha:latest .
docker push gcr.io/holomisha-project/holomisha:latest

# Apply Kubernetes manifests
kubectl apply -f kubernetes.yaml

# Run tests
pytest tests/ --cov=src --cov-report=html

# Monitor deployment
kubectl rollout status deployment/holomisha

echo "Deployment completed! 🌌"