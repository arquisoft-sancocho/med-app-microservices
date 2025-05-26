#!/bin/bash

# Script to update microservice URLs in core-medical-service
# This script can be run manually if needed for debugging or updates

set -e

PROJECT_ID="molten-avenue-460900-a0"
REGION="us-central1"

echo "🔗 Updating microservice URLs in core-medical-service..."
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

# Get the URLs for all microservices
echo "🔍 Getting microservice URLs..."

EXAMS_URL=$(gcloud run services describe exams-service --region=$REGION --format="value(status.url)" 2>/dev/null || echo "")
DIAGNOSIS_URL=$(gcloud run services describe diagnosis-service --region=$REGION --format="value(status.url)" 2>/dev/null || echo "")
SURGERY_URL=$(gcloud run services describe surgery-service --region=$REGION --format="value(status.url)" 2>/dev/null || echo "")
CORE_URL=$(gcloud run services describe core-medical-service --region=$REGION --format="value(status.url)" 2>/dev/null || echo "")

echo "📋 Current microservice URLs:"
echo "   Core Medical: ${CORE_URL:-'❌ Not found'}"
echo "   Exams Service: ${EXAMS_URL:-'❌ Not found'}"
echo "   Diagnosis Service: ${DIAGNOSIS_URL:-'❌ Not found'}"
echo "   Surgery Service: ${SURGERY_URL:-'❌ Not found'}"
echo ""

# Check if all required services are available
if [[ -z "$EXAMS_URL" || -z "$DIAGNOSIS_URL" || -z "$SURGERY_URL" || -z "$CORE_URL" ]]; then
    echo "❌ Error: One or more microservices are not deployed or not found"
    echo "Please ensure all microservices are deployed first"
    exit 1
fi

# Update core-medical-service with the microservice URLs
echo "🔄 Updating core-medical-service with microservice URLs..."

gcloud run services update core-medical-service \
    --region=$REGION \
    --update-env-vars="EXAMS_SERVICE_URL=$EXAMS_URL" \
    --update-env-vars="DIAGNOSIS_SERVICE_URL=$DIAGNOSIS_URL" \
    --update-env-vars="SURGERY_SERVICE_URL=$SURGERY_URL"

echo "✅ Core medical service updated successfully!"
echo ""

# Test the connections
echo "🧪 Testing microservice connections..."

# Wait a moment for the update to take effect
sleep 10

# Test health endpoints
echo "   Testing core medical health..."
if curl -s --max-time 10 "$CORE_URL/health/ready" > /dev/null; then
    echo "   ✅ Core medical service is healthy"
else
    echo "   ⚠️ Core medical service health check failed"
fi

echo "   Testing exams service health..."
if curl -s --max-time 10 "$EXAMS_URL/health/ready" > /dev/null; then
    echo "   ✅ Exams service is healthy"
else
    echo "   ⚠️ Exams service health check failed"
fi

echo "   Testing diagnosis service health..."
if curl -s --max-time 10 "$DIAGNOSIS_URL/health/ready" > /dev/null; then
    echo "   ✅ Diagnosis service is healthy"
else
    echo "   ⚠️ Diagnosis service health check failed"
fi

echo "   Testing surgery service health..."
if curl -s --max-time 10 "$SURGERY_URL/health/ready" > /dev/null; then
    echo "   ✅ Surgery service is healthy"
else
    echo "   ⚠️ Surgery service health check failed"
fi

echo ""
echo "🎯 Microservice URL update completed!"
echo ""
echo "📋 Updated URLs:"
echo "   EXAMS_SERVICE_URL=$EXAMS_URL"
echo "   DIAGNOSIS_SERVICE_URL=$DIAGNOSIS_URL"
echo "   SURGERY_SERVICE_URL=$SURGERY_URL"
echo ""
echo "🔗 You can access the core medical service at: $CORE_URL"
echo "🔑 To setup permissions, call: $CORE_URL/api/setup-permissions/"
echo "📊 To check permissions status: $CORE_URL/api/permissions-status/"
