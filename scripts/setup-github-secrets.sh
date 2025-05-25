#!/bin/bash

# Setup GitHub Secrets for Automated Deployment
# This script helps configure the necessary secrets for GitHub Actions

set -e

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

print_step "GitHub Secrets Configuration Guide"
echo "=============================================="

print_info "This script will help you configure the necessary secrets for GitHub Actions deployment."
print_warning "You need to manually add these secrets to your GitHub repository."

echo ""
print_step "1. Get Service Account Key (GCP_SA_KEY)"
echo "----------------------------------------"

if [ -f "/home/db/github-actions-key.json" ]; then
    print_info "Service account key found. Copy this entire JSON content:"
    echo ""
    echo "Secret Name: GCP_SA_KEY"
    echo "Secret Value:"
    echo "============="
    cat /home/db/github-actions-key.json
    echo ""
    echo "============="
else
    print_error "Service account key not found. Creating it..."
    gcloud iam service-accounts keys create /home/db/github-actions-key.json \
        --iam-account=github-actions@molten-avenue-460900-a0.iam.gserviceaccount.com

    print_info "Service account key created. Copy this entire JSON content:"
    echo ""
    echo "Secret Name: GCP_SA_KEY"
    echo "Secret Value:"
    echo "============="
    cat /home/db/github-actions-key.json
    echo ""
    echo "============="
fi

echo ""
print_step "2. Get JWT Secret Key (JWT_SECRET_KEY)"
echo "------------------------------------"

JWT_SECRET=$(gcloud secrets versions access latest --secret="jwt-secret-key" 2>/dev/null || echo "")

if [ -n "$JWT_SECRET" ]; then
    print_info "JWT secret found:"
    echo ""
    echo "Secret Name: JWT_SECRET_KEY"
    echo "Secret Value: $JWT_SECRET"
else
    print_warning "JWT secret not found. Creating a new one..."
    JWT_SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    echo "$JWT_SECRET" | gcloud secrets create jwt-secret-key --data-file=- || \
    echo "$JWT_SECRET" | gcloud secrets versions add jwt-secret-key --data-file=-

    print_info "JWT secret created:"
    echo ""
    echo "Secret Name: JWT_SECRET_KEY"
    echo "Secret Value: $JWT_SECRET"
fi

echo ""
print_step "3. How to Add Secrets to GitHub"
echo "================================"

print_info "Follow these steps to add the secrets to your GitHub repository:"
echo ""
echo "1. Go to your repository on GitHub"
echo "2. Click on 'Settings' tab"
echo "3. In the left sidebar, click 'Secrets and variables' → 'Actions'"
echo "4. Click 'New repository secret'"
echo "5. Add the following secrets one by one:"
echo ""
echo "   Secret 1:"
echo "   Name: GCP_SA_KEY"
echo "   Value: [Copy the entire JSON content from step 1 above]"
echo ""
echo "   Secret 2:"
echo "   Name: JWT_SECRET_KEY"
echo "   Value: $JWT_SECRET"
echo ""

print_step "4. Verify Database Secrets in Secret Manager"
echo "==========================================="

print_info "Checking existing database secrets..."

# Check if database secrets exist
DB_SECRETS=("core-db-password" "exams-db-password" "diagnosis-db-password" "surgery-db-password")

for secret in "${DB_SECRETS[@]}"; do
    if gcloud secrets describe "$secret" &>/dev/null; then
        print_info "✓ Secret '$secret' exists in Secret Manager"
    else
        print_warning "✗ Secret '$secret' not found. Creating with default password..."
        echo "medical123!" | gcloud secrets create "$secret" --data-file=-
        print_info "✓ Created secret '$secret' with default password"
    fi
done

echo ""
print_step "5. Repository Setup Verification"
echo "==============================="

print_info "Make sure your repository has the following structure:"
echo ""
echo "✓ .github/workflows/deploy-microservices.yml"
echo "✓ infrastructure/main.tf"
echo "✓ services/*/Dockerfile"
echo "✓ All microservice code"

echo ""
print_step "6. Trigger Deployment"
echo "==================="

print_info "Once you've added the secrets to GitHub, you can trigger deployment by:"
echo ""
echo "Option 1 - Push to main branch:"
echo "   git add ."
echo "   git commit -m 'Configure deployment with GitHub Actions'"
echo "   git push origin main"
echo ""
echo "Option 2 - Manual trigger:"
echo "   Go to Actions tab → Deploy Microservices to GCP → Run workflow"

echo ""
print_step "7. Monitor Deployment"
echo "==================="

print_info "After triggering the deployment:"
echo ""
echo "1. Go to the 'Actions' tab in your GitHub repository"
echo "2. Click on the running workflow"
echo "3. Monitor the build and deployment process"
echo "4. Check Cloud Run services in GCP Console"
echo "5. Verify Load Balancer configuration"

echo ""
print_warning "Important Notes:"
echo "• The first deployment may take 10-15 minutes"
echo "• SSL certificate provisioning can take additional time"
echo "• Monitor logs in both GitHub Actions and GCP Console"
echo "• Database migrations will run automatically"

echo ""
print_info "Setup guide completed!"
print_info "Repository: https://github.com/[your-username]/med-app-microservices"
print_info "Don't forget to add the secrets to GitHub before triggering deployment!"

# Cleanup
rm -f /home/db/github-actions-key.json
print_info "Service account key file cleaned up for security."
