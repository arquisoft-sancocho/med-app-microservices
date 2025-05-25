#!/bin/bash

# Pre-deployment Status Check
# This script verifies the current state of infrastructure before GitHub Actions deployment

set -e

# Configuration
PROJECT_ID="molten-avenue-460900-a0"
REGION="us-central1"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

echo "========================================"
print_step "Pre-deployment Infrastructure Status"
echo "========================================"

print_step "1. Checking GCP Authentication"
echo "-----------------------------"

if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "@"; then
    print_error "Not authenticated with gcloud"
    exit 1
fi

CURRENT_PROJECT=$(gcloud config get-value project)
print_info "✓ Authenticated with gcloud"
print_info "✓ Current project: $CURRENT_PROJECT"

if [ "$CURRENT_PROJECT" != "$PROJECT_ID" ]; then
    print_warning "Project mismatch. Setting to $PROJECT_ID"
    gcloud config set project $PROJECT_ID
fi

print_step "2. Checking Required APIs"
echo "------------------------"

REQUIRED_APIS=(
    "run.googleapis.com"
    "compute.googleapis.com"
    "artifactregistry.googleapis.com"
    "secretmanager.googleapis.com"
)

for api in "${REQUIRED_APIS[@]}"; do
    if gcloud services list --enabled --filter="name:$api" --format="value(name)" | grep -q "$api"; then
        print_info "✓ $api is enabled"
    else
        print_warning "✗ $api is not enabled"
        print_info "Enabling $api..."
        gcloud services enable "$api"
        print_info "✓ $api enabled"
    fi
done

print_step "3. Checking Cloud SQL Instances"
echo "------------------------------"

DB_INSTANCES=("core-medical-db" "exams-db" "diagnosis-db" "surgery-db")

for instance in "${DB_INSTANCES[@]}"; do
    if gcloud sql instances describe "$instance" --format="value(name)" &>/dev/null; then
        STATUS=$(gcloud sql instances describe "$instance" --format="value(state)")
        print_info "✓ $instance exists (Status: $STATUS)"
    else
        print_error "✗ $instance not found"
    fi
done

print_step "4. Checking Artifact Registry"
echo "----------------------------"

if gcloud artifacts repositories describe microservices --location=$REGION &>/dev/null; then
    print_info "✓ Artifact Registry repository 'microservices' exists"
else
    print_warning "✗ Artifact Registry repository not found"
    print_info "Creating repository..."
    gcloud artifacts repositories create microservices \
        --repository-format=docker \
        --location=$REGION \
        --description="Docker repository for medical microservices"
    print_info "✓ Repository created"
fi

print_step "5. Checking Secret Manager Secrets"
echo "---------------------------------"

SECRETS=("core-db-password" "exams-db-password" "diagnosis-db-password" "surgery-db-password" "jwt-secret-key")

for secret in "${SECRETS[@]}"; do
    if gcloud secrets describe "$secret" &>/dev/null; then
        print_info "✓ Secret '$secret' exists"
    else
        print_error "✗ Secret '$secret' not found"
    fi
done

print_step "6. Checking Service Account"
echo "--------------------------"

SA_EMAIL="github-actions@${PROJECT_ID}.iam.gserviceaccount.com"

if gcloud iam service-accounts describe "$SA_EMAIL" &>/dev/null; then
    print_info "✓ Service account 'github-actions' exists"

    # Check roles
    print_info "Checking IAM roles..."
    ROLES=$(gcloud projects get-iam-policy $PROJECT_ID --flatten="bindings[].members" --format="table(bindings.role)" --filter="bindings.members:$SA_EMAIL" | tail -n +2)

    echo "   Assigned roles:"
    while read -r role; do
        if [ -n "$role" ]; then
            print_info "   - $role"
        fi
    done <<< "$ROLES"
else
    print_error "✗ Service account 'github-actions' not found"
fi

print_step "7. Checking Current Cloud Run Services"
echo "------------------------------------"

SERVICES=("core-medical-service" "exams-service" "diagnosis-service" "surgery-service")

for service in "${SERVICES[@]}"; do
    if gcloud run services describe "$service" --region=$REGION &>/dev/null; then
        URL=$(gcloud run services describe "$service" --region=$REGION --format="value(status.url)")
        print_info "✓ $service exists at: $URL"
    else
        print_warning "✗ $service not deployed yet"
    fi
done

print_step "8. Checking Load Balancer Components"
echo "----------------------------------"

# Check if load balancer exists
if gcloud compute url-maps describe medical-microservices-lb &>/dev/null; then
    print_info "✓ Load balancer 'medical-microservices-lb' exists"

    # Get external IP
    if gcloud compute addresses describe medical-microservices-ip --global &>/dev/null; then
        LB_IP=$(gcloud compute addresses describe medical-microservices-ip --global --format="value(address)")
        print_info "✓ Load balancer IP: $LB_IP"
    else
        print_warning "✗ Load balancer IP not reserved"
    fi
else
    print_warning "✗ Load balancer not configured yet"
fi

print_step "9. Repository Configuration Check"
echo "-------------------------------"

# Check if we're in a git repository
if [ -d ".git" ]; then
    print_info "✓ Git repository detected"

    # Check for required files
    FILES_TO_CHECK=(
        ".github/workflows/deploy-microservices.yml"
        "infrastructure/main.tf"
        "services/core-medical-service/Dockerfile"
        "services/exams-service/Dockerfile"
        "services/diagnosis-service/Dockerfile"
        "services/surgery-service/Dockerfile"
    )

    for file in "${FILES_TO_CHECK[@]}"; do
        if [ -f "$file" ]; then
            print_info "✓ $file exists"
        else
            print_error "✗ $file missing"
        fi
    done

    # Check git remote
    if git remote -v | grep -q "origin"; then
        REMOTE_URL=$(git remote get-url origin)
        print_info "✓ Git remote configured: $REMOTE_URL"
    else
        print_warning "✗ No git remote configured"
    fi
else
    print_error "✗ Not in a git repository"
fi

print_step "10. Network Configuration"
echo "------------------------"

# Check if default network exists
if gcloud compute networks describe default &>/dev/null; then
    print_info "✓ Default VPC network exists"
else
    print_warning "✗ Default VPC network not found"
fi

# Check Cloud NAT (if exists)
if gcloud compute routers list --filter="region:($REGION)" --format="value(name)" | grep -q .; then
    print_info "✓ Cloud Router exists in region"
else
    print_warning "✗ No Cloud Router found (may be needed for private services)"
fi

echo ""
print_step "Summary"
echo "======="

print_info "Pre-deployment check completed!"

echo ""
print_step "Next Steps:"
echo "----------"
echo "1. Add the following secrets to your GitHub repository:"
echo "   - GCP_SA_KEY (Service Account JSON key)"
echo "   - JWT_SECRET_KEY (JWT secret for authentication)"
echo ""
echo "2. Push your code to trigger the GitHub Actions workflow:"
echo "   git add ."
echo "   git commit -m 'Deploy medical microservices with Load Balancer'"
echo "   git push origin main"
echo ""
echo "3. Monitor the deployment:"
echo "   - GitHub Actions: https://github.com/[your-repo]/actions"
echo "   - Cloud Run: https://console.cloud.google.com/run"
echo "   - Load Balancer: https://console.cloud.google.com/net-services/loadbalancing"

print_info "Ready for GitHub Actions deployment! 🚀"
