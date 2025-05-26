#!/bin/bash

# Test script to verify microservice deployment and URL configuration
# This script simulates what happens during the GitHub Actions deployment

set -e

PROJECT_ID="molten-avenue-460900-a0"
REGION="us-central1"

echo "🧪 Testing microservice deployment and URL configuration..."
echo "📍 Project: $PROJECT_ID"
echo "📍 Region: $REGION"
echo ""

# Check if gcloud is authenticated
if ! gcloud auth list --filter="status:ACTIVE" --format="value(account)" | grep -q "@"; then
    echo "❌ Error: gcloud is not authenticated"
    echo "Please run: gcloud auth login"
    exit 1
fi

# Set the project
gcloud config set project $PROJECT_ID

echo "🔍 Step 1: Checking if all microservices are deployed..."

# Check each service
services=("core-medical-service" "exams-service" "diagnosis-service" "surgery-service")
failed_services=()

for service in "${services[@]}"; do
    echo "   Checking $service..."
    if gcloud run services describe $service --region=$REGION --format="value(status.url)" &>/dev/null; then
        url=$(gcloud run services describe $service --region=$REGION --format="value(status.url)")
        echo "   ✅ $service is deployed: $url"
    else
        echo "   ❌ $service is not deployed"
        failed_services+=("$service")
    fi
done

if [ ${#failed_services[@]} -gt 0 ]; then
    echo "❌ The following services are not deployed: ${failed_services[*]}"
    echo "Please deploy them first using the GitHub Actions workflow"
    exit 1
fi

echo ""
echo "🔄 Step 2: Testing URL update process..."

# Get URLs
EXAMS_URL=$(gcloud run services describe exams-service --region=$REGION --format="value(status.url)")
DIAGNOSIS_URL=$(gcloud run services describe diagnosis-service --region=$REGION --format="value(status.url)")
SURGERY_URL=$(gcloud run services describe surgery-service --region=$REGION --format="value(status.url)")
CORE_URL=$(gcloud run services describe core-medical-service --region=$REGION --format="value(status.url)")

echo "📋 Retrieved URLs:"
echo "   EXAMS_SERVICE_URL=$EXAMS_URL"
echo "   DIAGNOSIS_SERVICE_URL=$DIAGNOSIS_URL"
echo "   SURGERY_SERVICE_URL=$SURGERY_URL"
echo "   CORE_SERVICE_URL=$CORE_URL"

echo ""
echo "🔄 Step 3: Updating core-medical-service environment variables..."

# Update core-medical-service with the microservice URLs
gcloud run services update core-medical-service \
    --region=$REGION \
    --update-env-vars="EXAMS_SERVICE_URL=$EXAMS_URL" \
    --update-env-vars="DIAGNOSIS_SERVICE_URL=$DIAGNOSIS_URL" \
    --update-env-vars="SURGERY_SERVICE_URL=$SURGERY_URL" \
    --quiet

echo "✅ Environment variables updated!"

echo ""
echo "🔄 Step 4: Waiting for service to restart..."
sleep 30

echo ""
echo "🧪 Step 5: Testing health endpoints..."

test_health() {
    local name=$1
    local url=$2
    echo "   Testing $name health..."
    if curl -s --max-time 10 "$url/health/ready" > /dev/null 2>&1; then
        echo "   ✅ $name is healthy"
        return 0
    else
        echo "   ⚠️ $name health check failed"
        return 1
    fi
}

# Test all health endpoints
test_health "Core Medical" "$CORE_URL"
test_health "Exams Service" "$EXAMS_URL"
test_health "Diagnosis Service" "$DIAGNOSIS_URL"
test_health "Surgery Service" "$SURGERY_URL"

echo ""
echo "🔄 Step 6: Testing microservice integration..."

echo "   Testing examenes list endpoint..."
if curl -s --max-time 15 "$CORE_URL/examenes/" -H "Accept: text/html" > /dev/null 2>&1; then
    echo "   ✅ Examenes endpoint is accessible"
else
    echo "   ⚠️ Examenes endpoint test failed"
fi

echo "   Testing diagnosticos list endpoint..."
if curl -s --max-time 15 "$CORE_URL/diagnosticos/" -H "Accept: text/html" > /dev/null 2>&1; then
    echo "   ✅ Diagnosticos endpoint is accessible"
else
    echo "   ⚠️ Diagnosticos endpoint test failed"
fi

echo "   Testing cirugias list endpoint..."
if curl -s --max-time 15 "$CORE_URL/cirugias/" -H "Accept: text/html" > /dev/null 2>&1; then
    echo "   ✅ Cirugias endpoint is accessible"
else
    echo "   ⚠️ Cirugias endpoint test failed"
fi

echo ""
echo "🔄 Step 7: Testing permissions setup..."

echo "   Calling permissions setup API..."
setup_response=$(curl -s --max-time 60 -X POST "$CORE_URL/api/setup-permissions/" \
    -H "Content-Type: application/json" \
    -d '{"force": true}' \
    -w "%{http_code}" \
    -o /tmp/setup_response.json 2>/dev/null || echo "000")

if [ "$setup_response" -eq 200 ] || [ "$setup_response" -eq 201 ]; then
    echo "   ✅ Permissions setup successful (HTTP $setup_response)"
    if [ -f /tmp/setup_response.json ]; then
        echo "   📄 Response: $(cat /tmp/setup_response.json)"
    fi
else
    echo "   ⚠️ Permissions setup returned HTTP $setup_response"
    if [ -f /tmp/setup_response.json ]; then
        echo "   📄 Response: $(cat /tmp/setup_response.json)"
    fi
fi

echo ""
echo "   Checking permissions status..."
status_response=$(curl -s --max-time 30 "$CORE_URL/api/permissions-status/" 2>/dev/null || echo "Failed to get status")
echo "   📊 Permissions Status: $status_response"

echo ""
echo "🎯 Test Results Summary:"
echo "   📍 Load Balancer IP: $(cd infrastructure && terraform output -raw load_balancer_ip 2>/dev/null || echo 'Not available')"
echo "   🔗 Core Medical: $CORE_URL"
echo "   🔗 Exams Service: $EXAMS_URL"
echo "   🔗 Diagnosis Service: $DIAGNOSIS_URL"
echo "   🔗 Surgery Service: $SURGERY_URL"
echo ""
echo "📋 Access URLs:"
echo "   Main Application: $CORE_URL"
echo "   Examenes: $CORE_URL/examenes/"
echo "   Diagnosticos: $CORE_URL/diagnosticos/"
echo "   Cirugias: $CORE_URL/cirugias/"
echo "   Permissions Status: $CORE_URL/api/permissions-status/"

echo ""
echo "✅ Test completed! All microservices should now have correct URLs configured."

# Clean up temporary files
rm -f /tmp/setup_response.json
