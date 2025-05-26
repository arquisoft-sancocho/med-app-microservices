#!/bin/bash

# Deploy Medical Microservices to GCP - FIXED VERSION
# This script deploys microservices in correct order and configures URLs automatically
# 1. Deploy independent services first (exams, diagnosis, surgery)
# 2. Get their URLs and configure core-medical-service with proper environment variables

set -e

# Configuration
PROJECT_ID="molten-avenue-460900-a0"
REGION="us-central1"
GAR_LOCATION="us-central1-docker.pkg.dev"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if gcloud is authenticated
print_status "Checking gcloud authentication..."
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "@"; then
    print_error "Not authenticated with gcloud. Run 'gcloud auth login' first."
    exit 1
fi

# Set project
print_status "Setting project to $PROJECT_ID..."
gcloud config set project $PROJECT_ID

# Enable required APIs
print_status "Enabling required APIs..."
gcloud services enable run.googleapis.com
gcloud services enable compute.googleapis.com
gcloud services enable artifactregistry.googleapis.com

# Create Artifact Registry repository if it doesn't exist
print_status "Creating Artifact Registry repository..."
gcloud artifacts repositories create microservices \
    --repository-format=docker \
    --location=$REGION \
    --description="Docker repository for medical microservices" || true

# Configure Docker to use gcloud as credential helper
print_status "Configuring Docker authentication..."
gcloud auth configure-docker $GAR_LOCATION

# Array of services
declare -a services=(
    "core-medical-service:core_medical"
    "exams-service:exams_db"
    "diagnosis-service:diagnosis_db"
    "surgery-service:surgery_db"
)

# Build and deploy each service
for service_info in "${services[@]}"; do
    IFS=':' read -r service_name db_name <<< "$service_info"

    print_status "Building and deploying $service_name..."

    # Navigate to service directory
    cd services/$service_name

    # Build Docker image
    print_status "Building Docker image for $service_name..."
    docker build -t $GAR_LOCATION/$PROJECT_ID/microservices/$service_name:latest .

    # Push image
    print_status "Pushing image for $service_name..."
    docker push $GAR_LOCATION/$PROJECT_ID/microservices/$service_name:latest

    # Get the corresponding Cloud SQL instance name
    case $service_name in
        "core-medical-service")
            sql_instance="core-medical-db"
            ;;
        "exams-service")
            sql_instance="exams-db"
            ;;
        "diagnosis-service")
            sql_instance="diagnosis-db"
            ;;
        "surgery-service")
            sql_instance="surgery-db"
            ;;
    esac

    # Deploy to Cloud Run
    print_status "Deploying $service_name to Cloud Run..."
    gcloud run deploy $service_name \
        --image=$GAR_LOCATION/$PROJECT_ID/microservices/$service_name:latest \
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
        --update-secrets="DB_PASSWORD=${sql_instance//-/_}_password:latest" \
        --startup-probe="httpGet.path=/health/ready,initialDelaySeconds=10,timeoutSeconds=5,periodSeconds=10,failureThreshold=3" \
        --liveness-probe="httpGet.path=/health/live,initialDelaySeconds=30,timeoutSeconds=5,periodSeconds=30,failureThreshold=3"

    # Make service publicly accessible
    print_status "Making $service_name publicly accessible..."
    gcloud run services add-iam-policy-binding $service_name \
        --member="allUsers" \
        --role="roles/run.invoker" \
        --region=$REGION

    # Go back to root directory
    cd ../..

    print_status "$service_name deployed successfully!"
done

# Deploy Load Balancer using Terraform
print_status "Deploying Load Balancer configuration..."
cd infrastructure

# Initialize Terraform
terraform init

# Plan deployment
print_status "Planning Terraform deployment..."
terraform plan -var="project_id=$PROJECT_ID" -var="region=$REGION"

# Apply configuration
print_status "Applying Terraform configuration..."
terraform apply -auto-approve -var="project_id=$PROJECT_ID" -var="region=$REGION"

# Get outputs
print_status "Getting deployment information..."
LB_IP=$(terraform output -raw load_balancer_ip)

cd ..

print_status "Deployment completed successfully!"
print_status "Load Balancer IP: $LB_IP"
print_status ""
print_status "Service URLs:"

# Get Cloud Run service URLs
for service_info in "${services[@]}"; do
    IFS=':' read -r service_name db_name <<< "$service_info"
    SERVICE_URL=$(gcloud run services describe $service_name --region=$REGION --format="value(status.url)")
    print_status "  $service_name: $SERVICE_URL"
done

print_status ""
print_status "API Gateway will be available at: https://$LB_IP"
print_warning "Note: SSL certificate may take a few minutes to provision."
print_warning "Update your DNS records to point to $LB_IP"

print_status ""
print_status "Testing endpoints:"
print_status "  Health checks: https://$LB_IP/health/ready"
print_status "  API docs: https://$LB_IP/api/"
print_status "  Admin: https://$LB_IP/admin/"
