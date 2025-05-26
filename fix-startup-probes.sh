#!/bin/bash

# Startup Probe Fix for Django Microservices
# This script addresses the startup probe timeout issues in Cloud Run

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "\n${BLUE}=== $1 ===${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

PROJECT_ID="molten-avenue-460900-a0"
REGION="us-central1"

print_header "Django Microservices Startup Probe Fix"
echo "Deploying services with optimized health probe configurations..."
echo "Date: $(date)"

# Optimized probe settings for Django applications
# Django apps need more time to:
# 1. Start gunicorn server
# 2. Connect to Cloud SQL database
# 3. Load Django settings and middleware
# 4. Initialize application modules

STARTUP_PROBE="httpGet.path=/health/ready,initialDelaySeconds=30,timeoutSeconds=10,periodSeconds=15,failureThreshold=5"
LIVENESS_PROBE="httpGet.path=/health/live,initialDelaySeconds=60,timeoutSeconds=10,periodSeconds=30,failureThreshold=3"

# Services to deploy with fixed probe settings
declare -a SERVICES=("core-medical-service" "diagnosis-service" "exams-service" "surgery-service")

for service in "${SERVICES[@]}"; do
    print_header "Deploying $service with optimized probe settings"
    
    if [ -d "services/$service" ]; then
        cd "services/$service"
        
        print_warning "Deploying with probe settings:"
        echo "  Startup Probe: 30s initial delay, 10s timeout, 15s period, 5 failures = ~2 minutes max startup time"
        echo "  Liveness Probe: 60s initial delay, 10s timeout, 30s period, 3 failures"
        
        gcloud run deploy "$service" \
            --source . \
            --region="$REGION" \
            --platform=managed \
            --allow-unauthenticated \
            --port=8080 \
            --memory=1Gi \
            --cpu=1 \
            --min-instances=0 \
            --max-instances=10 \
            --timeout=300 \
            --startup-probe="$STARTUP_PROBE" \
            --liveness-probe="$LIVENESS_PROBE" || {
                print_error "Failed to deploy $service"
                cd ../..
                continue
            }
        
        print_success "$service deployed successfully"
        cd ../..
    else
        print_error "Directory services/$service not found"
    fi
done

print_header "Deployment Summary"
echo "All services have been deployed with optimized startup probe configurations."
echo "The new settings allow up to 2 minutes for application startup, which should"
echo "be sufficient for Django applications connecting to Cloud SQL databases."

print_header "Startup Probe Analysis"
echo "Previous settings (causing failures):"
echo "  - initialDelaySeconds: 10"
echo "  - timeoutSeconds: 5" 
echo "  - periodSeconds: 10"
echo "  - failureThreshold: 3"
echo "  - Total startup time: ~40 seconds maximum"
echo ""
echo "New optimized settings:"
echo "  - initialDelaySeconds: 30 (wait 30s before first check)"
echo "  - timeoutSeconds: 10 (each request has 10s to complete)"
echo "  - periodSeconds: 15 (check every 15 seconds)"
echo "  - failureThreshold: 5 (allow 5 failures before giving up)"
echo "  - Total startup time: 30s + (15s × 5) = 105 seconds maximum"
echo ""
echo "This gives Django applications sufficient time to:"
echo "  1. Start gunicorn server"
echo "  2. Establish Cloud SQL database connections"
echo "  3. Load Django settings and middleware"
echo "  4. Initialize all application modules"
echo "  5. Respond to health check requests"

print_success "Startup probe configuration fix completed!"
