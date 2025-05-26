#!/bin/bash
# Test script for FastAPI Exams Service

echo "=== FastAPI Exams Service Test Script ==="

# Check if service is running
SERVICE_URL="http://localhost:8080"

echo "Testing service at: $SERVICE_URL"

# Test health endpoints
echo "1. Testing health endpoints..."
curl -s "$SERVICE_URL/health/live" | jq . || echo "Health check failed"
curl -s "$SERVICE_URL/health/ready" | jq . || echo "Ready check failed"

# Test root endpoint
echo "2. Testing root endpoint..."
curl -s "$SERVICE_URL/" | jq . || echo "Root endpoint failed"

# Test public API
echo "3. Testing public API..."
curl -s "$SERVICE_URL/public-api/examenes/" | jq . || echo "Public API failed"

# Test main API
echo "4. Testing main API..."
curl -s "$SERVICE_URL/api/examenes/" | jq . || echo "Main API failed"

# Test exam creation (example)
echo "5. Testing exam creation..."
curl -X POST "$SERVICE_URL/api/examenes/" \
  -H "Content-Type: multipart/form-data" \
  -F "nombre=Test Exam" \
  -F "paciente_id=1" \
  -F "descripcion=Test description" \
  -F "tipo_examen=sangre" \
  -F "fecha_examen=2024-12-01" \
  | jq . || echo "Exam creation failed"

echo "=== Test completed ==="
