#!/bin/bash

# Fixed Deploy Script - Deploy microservices with proper URL configuration
# This script deploys services in the correct order and configures microservice URLs

set -e

# Configuration
PROJECT_ID="molten-avenue-460900-a0"
REGION="us-central1"
GAR_LOCATION="us-central1-docker.pkg.dev"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step "MICROSERVICES DEPLOYMENT WITH URL CONFIGURATION"
echo "==============================================="

# Change to root directory
cd /home/db/University/arquisoft/med-app-microservices

print_status "Setting project to $PROJECT_ID..."
gcloud config set project $PROJECT_ID

# Phase 1: Deploy independent microservices first
print_step "Phase 1: Deploying Independent Microservices"
echo "=============================================="

# Array of independent services (services that don't call other microservices)
declare -a independent_services=(
    "exams-service:exams_db:exams-db"
    "diagnosis-service:diagnosis_db:diagnosis-db"
    "surgery-service:surgery_db:surgery-db"
)

# Deploy independent services first
for service_info in "${independent_services[@]}"; do
    IFS=':' read -r service_name db_name sql_instance <<< "$service_info"

    print_status "Building and deploying $service_name..."

    # Navigate to service directory
    cd services/$service_name

    # Build and deploy
    print_status "Building image for $service_name..."
    gcloud builds submit --tag gcr.io/$PROJECT_ID/microservices/$service_name:latest .

    print_status "Deploying $service_name to Cloud Run..."
    gcloud run deploy $service_name \
        --image=gcr.io/$PROJECT_ID/microservices/$service_name:latest \
        --region=$REGION \
        --platform=managed \
        --allow-unauthenticated \
        --port=8080 \
        --memory=1Gi \
        --cpu=1 \
        --min-instances=0 \
        --max-instances=10 \
        --timeout=300 \
        --add-cloudsql-instances=$PROJECT_ID:$REGION:$sql_instance \
        --set-env-vars="DEBUG=False,ALLOWED_HOSTS=*,DB_NAME=$db_name,DB_USER=postgres,DB_HOST=/cloudsql/$PROJECT_ID:$REGION:$sql_instance" \
        --update-secrets="DB_PASSWORD=${sql_instance}-password:latest" \
        --startup-probe="httpGet.path=/health/ready,initialDelaySeconds=30,timeoutSeconds=10,periodSeconds=15,failureThreshold=5" \
        --liveness-probe="httpGet.path=/health/live,initialDelaySeconds=60,timeoutSeconds=10,periodSeconds=30,failureThreshold=3"

    print_status "Making $service_name publicly accessible..."
    gcloud run services add-iam-policy-binding $service_name \
        --member="allUsers" \
        --role="roles/run.invoker" \
        --region=$REGION

    cd ../..
    print_status "✅ $service_name deployed successfully!"
done

# Phase 2: Get URLs of deployed services
print_step "Phase 2: Getting Microservice URLs"
echo "=================================="

print_status "Retrieving deployed service URLs..."

EXAMS_SERVICE_URL=$(gcloud run services describe exams-service --region=$REGION --format="value(status.url)")
DIAGNOSIS_SERVICE_URL=$(gcloud run services describe diagnosis-service --region=$REGION --format="value(status.url)")
SURGERY_SERVICE_URL=$(gcloud run services describe surgery-service --region=$REGION --format="value(status.url)")

print_status "Retrieved URLs:"
echo "  📋 Exams Service:     $EXAMS_SERVICE_URL"
echo "  🩺 Diagnosis Service: $DIAGNOSIS_SERVICE_URL"
echo "  🏥 Surgery Service:   $SURGERY_SERVICE_URL"

# Validate URLs
if [[ -z "$EXAMS_SERVICE_URL" || -z "$DIAGNOSIS_SERVICE_URL" || -z "$SURGERY_SERVICE_URL" ]]; then
    print_error "Failed to retrieve all service URLs. Cannot proceed with core service deployment."
    exit 1
fi

# Phase 3: Deploy core-medical-service with microservice URLs
print_step "Phase 3: Deploying Core Medical Service with Microservice URLs"
echo "=============================================================="

print_status "Building and deploying core-medical-service with microservice URLs..."

cd services/core-medical-service

print_status "Building image for core-medical-service..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/microservices/core-medical-service:latest .

print_status "Deploying core-medical-service with microservice configuration..."
gcloud run deploy core-medical-service \
    --image=gcr.io/$PROJECT_ID/microservices/core-medical-service:latest \
    --region=$REGION \
    --platform=managed \
    --allow-unauthenticated \
    --port=8080 \
    --memory=1Gi \
    --cpu=1 \
    --min-instances=0 \
    --max-instances=10 \
    --timeout=300 \
    --add-cloudsql-instances=$PROJECT_ID:$REGION:core-medical-db \
    --set-env-vars="DEBUG=False,ALLOWED_HOSTS=*,DB_NAME=core_medical,DB_USER=postgres,DB_HOST=/cloudsql/$PROJECT_ID:$REGION:core-medical-db,EXAMS_SERVICE_URL=$EXAMS_SERVICE_URL,DIAGNOSIS_SERVICE_URL=$DIAGNOSIS_SERVICE_URL,SURGERY_SERVICE_URL=$SURGERY_SERVICE_URL" \
    --update-secrets="DB_PASSWORD=core-db-password:latest" \
    --startup-probe="httpGet.path=/health/ready,initialDelaySeconds=30,timeoutSeconds=10,periodSeconds=15,failureThreshold=5" \
    --liveness-probe="httpGet.path=/health/live,initialDelaySeconds=60,timeoutSeconds=10,periodSeconds=30,failureThreshold=3"

print_status "Making core-medical-service publicly accessible..."
gcloud run services add-iam-policy-binding core-medical-service \
    --member="allUsers" \
    --role="roles/run.invoker" \
    --region=$REGION

cd ../..

# Phase 4: Get final service information
print_step "Phase 4: Deployment Summary"
echo "==========================="

CORE_SERVICE_URL=$(gcloud run services describe core-medical-service --region=$REGION --format="value(status.url)")

print_status "✅ All services deployed successfully!"
echo ""
echo "📊 DEPLOYED SERVICES:"
echo "===================="
echo "🏥 Core Medical Service:  $CORE_SERVICE_URL"
echo "📋 Exams Service:         $EXAMS_SERVICE_URL"
echo "🩺 Diagnosis Service:     $DIAGNOSIS_SERVICE_URL"
echo "🏥 Surgery Service:       $SURGERY_SERVICE_URL"
echo ""

print_step "Phase 5: Testing Microservice Communication"
echo "==========================================="

print_status "Testing service health endpoints..."

# Test each service
services=("$CORE_SERVICE_URL" "$EXAMS_SERVICE_URL" "$DIAGNOSIS_SERVICE_URL" "$SURGERY_SERVICE_URL")
service_names=("Core" "Exams" "Diagnosis" "Surgery")

for i in "${!services[@]}"; do
    service_url="${services[$i]}"
    service_name="${service_names[$i]}"

    if curl -s -f "$service_url/health/ready" > /dev/null; then
        print_status "✅ $service_name Service: Health check passed"
    else
        print_warning "⚠️  $service_name Service: Health check failed"
    fi
done

echo ""
print_step "DEPLOYMENT COMPLETED"
echo "===================="
echo ""
print_status "🎉 Microservices deployment completed with proper URL configuration!"
print_status ""
print_status "Now when you access:"
print_status "  $CORE_SERVICE_URL/examenes/ → Will redirect to $EXAMS_SERVICE_URL"
print_status "  $CORE_SERVICE_URL/diagnosticos/ → Will redirect to $DIAGNOSIS_SERVICE_URL"
print_status "  $CORE_SERVICE_URL/cirugias/ → Will redirect to $SURGERY_SERVICE_URL"
print_status ""
print_warning "Note: This resolves the localhost:8001 redirect issue!"
