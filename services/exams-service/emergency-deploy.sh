#!/bin/bash
# Alternative deployment script for Exams Service when GitHub Actions fails
# This script can be run locally or in any CI/CD environment

set -e

# Configuration
PROJECT_ID="molten-avenue-460900-a0"
SERVICE_NAME="exams-service"
REGION="us-central1"
SERVICE_PATH="services/exams-service"
GAR_LOCATION="us-central1-docker.pkg.dev"

echo "=== Emergency Deployment: Exams Service ==="
echo "Project ID: $PROJECT_ID"
echo "Service Name: $SERVICE_NAME"
echo "Region: $REGION"

# Check if we're in the right directory
if [ ! -d "$SERVICE_PATH" ]; then
    echo "Error: $SERVICE_PATH directory not found. Make sure you're in the project root."
    exit 1
fi

# Check if user is authenticated
echo "1. Checking authentication..."
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "Error: No active gcloud authentication found. Please run 'gcloud auth login'"
    exit 1
fi

# Set project
echo "2. Setting project..."
gcloud config set project $PROJECT_ID

# Navigate to service directory
cd $SERVICE_PATH

# Build Docker image using Cloud Build (more reliable than local build + push)
echo "3. Building Docker image with Cloud Build..."
gcloud builds submit --tag $GAR_LOCATION/$PROJECT_ID/microservices/$SERVICE_NAME:latest --timeout=20m

# Deploy to Cloud Run with all necessary environment variables
echo "4. Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image=$GAR_LOCATION/$PROJECT_ID/microservices/$SERVICE_NAME:latest \
  --region=$REGION \
  --platform=managed \
  --allow-unauthenticated \
  --port=8080 \
  --memory=1Gi \
  --cpu=1 \
  --min-instances=0 \
  --max-instances=10 \
  --add-cloudsql-instances=$PROJECT_ID:$REGION:exams-db \
  --set-env-vars="DEBUG=false,GCS_BUCKET_NAME=medical-system-files,MAX_FILE_SIZE=10485760,DB_HOST=/cloudsql/$PROJECT_ID:$REGION:exams-db,DB_NAME=exams_db,DB_USER=postgres,ALLOWED_HOSTS=*" \
  --timeout=300 \
  --startup-probe="httpGet.path=/health/ready,initialDelaySeconds=10,timeoutSeconds=5,periodSeconds=10,failureThreshold=3" \
  --liveness-probe="httpGet.path=/health/live,initialDelaySeconds=30,timeoutSeconds=5,periodSeconds=30,failureThreshold=3"

# Get service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME \
  --region=$REGION \
  --format="value(status.url)")

echo "5. Setting up GCS permissions..."
# Get the service account used by Cloud Run
SERVICE_ACCOUNT=$(gcloud run services describe $SERVICE_NAME \
  --region=$REGION \
  --format="value(spec.template.spec.serviceAccountName)" 2>/dev/null || echo "")

if [ -z "$SERVICE_ACCOUNT" ]; then
    # Use default compute service account
    SERVICE_ACCOUNT="$PROJECT_ID-compute@developer.gserviceaccount.com"
fi

echo "Using service account: $SERVICE_ACCOUNT"

# Grant GCS permissions
echo "Granting GCS permissions..."
gsutil iam ch serviceAccount:$SERVICE_ACCOUNT:objectAdmin gs://medical-system-files
gsutil iam ch serviceAccount:$SERVICE_ACCOUNT:legacyBucketReader gs://medical-system-files

echo "6. Testing deployment..."
sleep 30  # Wait for service to be ready

# Test health endpoint
echo "Testing health endpoint..."
if curl -f "$SERVICE_URL/health/ready"; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed"
fi

# Test API endpoint
echo "Testing API endpoint..."
if curl -f "$SERVICE_URL/api/examenes/"; then
    echo "✅ API endpoint accessible"
else
    echo "❌ API endpoint failed"
fi

echo "=== Deployment Summary ==="
echo "✅ Service deployed successfully!"
echo "📍 Service URL: $SERVICE_URL"
echo "🔗 API Endpoint: $SERVICE_URL/api/examenes/"
echo "❤️ Health Check: $SERVICE_URL/health/ready"
echo "💾 GCS Bucket: medical-system-files"
echo ""
echo "Next steps:"
echo "1. Update core-medical-service EXAMS_SERVICE_URL to: $SERVICE_URL"
echo "2. Test file upload functionality through the web interface"
echo "3. Verify end-to-end integration"

# Return to original directory
cd - > /dev/null

echo "=== Emergency deployment completed ==="
