#!/bin/bash

# Deploy to GCP using GitHub Actions
# This script commits changes and triggers the automated deployment

set -e

# Colors for output
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

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

echo "========================================"
print_step "GitHub Actions Deployment Trigger"
echo "========================================"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    print_warning "Not in a git repository. Initializing..."
    git init
    print_info "Git repository initialized"
fi

# Check for GitHub remote
if ! git remote get-url origin &>/dev/null; then
    print_warning "No GitHub remote configured."
    echo "Please add your GitHub repository as origin:"
    echo "git remote add origin https://github.com/[your-username]/med-app-microservices.git"
    exit 1
fi

REMOTE_URL=$(git remote get-url origin)
print_info "GitHub remote: $REMOTE_URL"

print_step "1. Checking GitHub Secrets Configuration"
echo "--------------------------------------"

print_warning "IMPORTANT: Make sure you have added these secrets to GitHub:"
echo ""
echo "Secret 1: GCP_SA_KEY"
echo "Secret 2: JWT_SECRET_KEY"
echo ""
echo "To add secrets:"
echo "1. Go to your repository on GitHub"
echo "2. Settings → Secrets and variables → Actions"
echo "3. Click 'New repository secret'"
echo ""
read -p "Have you added the secrets to GitHub? (y/N): " -r
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_warning "Please add the secrets first, then run this script again."
    exit 1
fi

print_step "2. Preparing Repository for Deployment"
echo "------------------------------------"

# Add all files
print_info "Adding all files to git..."
git add .

# Check if there are changes to commit
if git diff --cached --quiet; then
    print_info "No changes to commit"
else
    print_info "Changes detected, creating commit..."

    # Create commit message
    COMMIT_MSG="Deploy medical microservices to GCP with Load Balancer

- Configure GitHub Actions workflow for automated deployment
- Set up Terraform for Load Balancer configuration
- Optimize Docker containers with multi-stage builds
- Configure Cloud Run services with health checks
- Set up microservices communication and routing

Services included:
- Core Medical Service (patients, consultations, auth)
- Exams Service (medical examinations)
- Diagnosis Service (diagnosis management)
- Surgery Service (surgery management)

Infrastructure:
- Google Cloud Run for container hosting
- Google Load Balancer for traffic routing
- Cloud SQL for databases
- Artifact Registry for container images
- Secret Manager for sensitive data"

    git commit -m "$COMMIT_MSG"
    print_info "✓ Commit created"
fi

print_step "3. Pushing to GitHub (Triggering Deployment)"
echo "------------------------------------------"

print_info "Pushing to main branch..."
git push origin main

print_info "✓ Code pushed to GitHub!"

print_step "4. Monitoring Deployment"
echo "----------------------"

echo ""
print_info "Deployment has been triggered! 🚀"
echo ""
echo "Monitor the deployment progress:"
echo "1. GitHub Actions: ${REMOTE_URL/\.git/}/actions"
echo "2. Expected deployment time: 10-15 minutes"
echo "3. Cloud Run console: https://console.cloud.google.com/run"
echo "4. Load Balancer console: https://console.cloud.google.com/net-services/loadbalancing"
echo ""

print_step "5. What's Being Deployed"
echo "----------------------"

echo "Microservices:"
echo "✓ core-medical-service (Patients, Consultations, Auth)"
echo "✓ exams-service (Medical Examinations)"
echo "✓ diagnosis-service (Diagnosis Management)"
echo "✓ surgery-service (Surgery Management)"
echo ""

echo "Infrastructure:"
echo "✓ Cloud Run services with auto-scaling"
echo "✓ Global Load Balancer with SSL"
echo "✓ Network Endpoint Groups (NEGs)"
echo "✓ Health checks and probes"
echo "✓ Database connections to Cloud SQL"
echo ""

print_step "6. Post-Deployment Steps"
echo "----------------------"

echo "After deployment completes:"
echo "1. Get the Load Balancer IP address"
echo "2. Configure DNS records (if needed)"
echo "3. Test the API endpoints"
echo "4. Verify SSL certificate provisioning"
echo "5. Monitor application logs"
echo ""

echo "Useful commands after deployment:"
echo "# Get Load Balancer IP"
echo "gcloud compute addresses describe medical-microservices-ip --global --format='value(address)'"
echo ""
echo "# Test health endpoints"
echo "curl https://[LB-IP]/health/ready"
echo ""
echo "# View Cloud Run services"
echo "gcloud run services list --region=us-central1"
echo ""

print_info "Deployment initiated successfully!"
print_info "Check GitHub Actions for real-time progress: ${REMOTE_URL/\.git/}/actions"
