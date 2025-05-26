#!/bin/bash
# Build and deploy script for FastAPI Exams Service

set -e

PROJECT_ID=${1:-"your-project-id"}
SERVICE_NAME="exams-service"
REGION="us-central1"
IMAGE_TAG="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "=== Building and Deploying FastAPI Exams Service ==="
echo "Project ID: $PROJECT_ID"
echo "Service Name: $SERVICE_NAME"
echo "Region: $REGION"
echo "Image Tag: $IMAGE_TAG"

# Navigate to service directory
cd "$(dirname "$0")"

# Build Docker image using Cloud Build
echo "1. Building Docker image with Cloud Build..."
gcloud builds submit --tag $IMAGE_TAG --project $PROJECT_ID

# Deploy to Cloud Run
echo "2. Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE_TAG \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --timeout 60 \
  --concurrency 100 \
  --max-instances 10 \
  --set-env-vars "DEBUG=false,GCS_BUCKET_NAME=medical-system-files,MAX_FILE_SIZE=10485760" \
  --project $PROJECT_ID

# Get service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --format "value(status.url)" \
  --project $PROJECT_ID)

echo "3. Service deployed successfully!"
echo "Service URL: $SERVICE_URL"

# Test health endpoint
echo "5. Testing health endpoint..."
sleep 10  # Wait for service to be ready
curl -f "$SERVICE_URL/health/ready" || echo "Health check failed"

echo "=== Deployment completed ==="
echo "Next steps:"
echo "1. Update EXAMS_SERVICE_URL in core-medical-service"
echo "2. Test integration with core service"
echo "3. Update load balancer configuration"
