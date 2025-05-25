#!/bin/bash

# Test script for Medical Microservices
# Tests JWT authentication and inter-service communication

set -e

# Configuration
CORE_SERVICE="http://localhost:8000"
EXAMS_SERVICE="http://localhost:8001"
DIAGNOSIS_SERVICE="http://localhost:8002"
SURGERY_SERVICE="http://localhost:8003"

# Test credentials
USERNAME="admin"
PASSWORD="admin123"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_test() {
    echo -e "${BLUE}[TEST]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

print_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
}

print_info() {
    echo -e "${YELLOW}[INFO]${NC} $1"
}

# Function to test service health
test_health() {
    local service_name=$1
    local service_url=$2

    print_test "Testing $service_name health checks..."

    # Test readiness probe
    if curl -s -f "$service_url/health/ready" > /dev/null; then
        print_success "$service_name readiness check passed"
    else
        print_fail "$service_name readiness check failed"
        return 1
    fi

    # Test liveness probe
    if curl -s -f "$service_url/health/live" > /dev/null; then
        print_success "$service_name liveness check passed"
    else
        print_fail "$service_name liveness check failed"
        return 1
    fi
}

# Function to get JWT token
get_jwt_token() {
    print_test "Getting JWT token from core service..."

    local response=$(curl -s -X POST "$CORE_SERVICE/auth/login/" \
        -H "Content-Type: application/json" \
        -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}")

    if [ $? -eq 0 ]; then
        local token=$(echo $response | grep -o '"token":"[^"]*"' | cut -d'"' -f4)
        if [ -n "$token" ]; then
            print_success "JWT token obtained successfully"
            echo $token
            return 0
        fi
    fi

    print_fail "Failed to get JWT token"
    print_info "Response: $response"
    return 1
}

# Function to test authenticated API call
test_authenticated_api() {
    local service_name=$1
    local service_url=$2
    local endpoint=$3
    local token=$4

    print_test "Testing authenticated API call to $service_name$endpoint..."

    local response=$(curl -s -H "Authorization: Bearer $token" "$service_url$endpoint")
    local status_code=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $token" "$service_url$endpoint")

    if [ "$status_code" -eq 200 ]; then
        print_success "$service_name API call successful"
        return 0
    else
        print_fail "$service_name API call failed (Status: $status_code)"
        print_info "Response: $response"
        return 1
    fi
}

# Function to test patient data consistency
test_patient_data() {
    local token=$1

    print_test "Testing patient data consistency across services..."

    # Get patient from core service
    local core_response=$(curl -s -H "Authorization: Bearer $token" "$CORE_SERVICE/api/patients/")

    if echo "$core_response" | grep -q "results"; then
        print_success "Patient data retrieved from core service"

        # Extract first patient ID
        local patient_id=$(echo "$core_response" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)

        if [ -n "$patient_id" ]; then
            print_info "Testing with patient ID: $patient_id"

            # Test exams for this patient
            test_authenticated_api "Exams Service" "$EXAMS_SERVICE" "/api/examenes/?paciente_id=$patient_id" "$token"

            # Test diagnosis for this patient
            test_authenticated_api "Diagnosis Service" "$DIAGNOSIS_SERVICE" "/api/diagnosticos/?paciente_id=$patient_id" "$token"

            # Test surgeries for this patient
            test_authenticated_api "Surgery Service" "$SURGERY_SERVICE" "/api/cirugias/by_patient/?patient_id=$patient_id" "$token"
        else
            print_fail "No patient ID found in core service response"
        fi
    else
        print_fail "Failed to get patient data from core service"
        print_info "Response: $core_response"
    fi
}

# Main test execution
main() {
    echo "=========================================="
    echo "Medical Microservices Test Suite"
    echo "=========================================="

    # Test 1: Health checks for all services
    print_info "Phase 1: Health Checks"
    test_health "Core Medical Service" "$CORE_SERVICE"
    test_health "Exams Service" "$EXAMS_SERVICE"
    test_health "Diagnosis Service" "$DIAGNOSIS_SERVICE"
    test_health "Surgery Service" "$SURGERY_SERVICE"

    echo ""

    # Test 2: JWT Authentication
    print_info "Phase 2: JWT Authentication"
    JWT_TOKEN=$(get_jwt_token)

    if [ $? -ne 0 ]; then
        print_fail "JWT authentication failed. Cannot continue with API tests."
        exit 1
    fi

    echo ""

    # Test 3: Authenticated API calls
    print_info "Phase 3: Authenticated API Calls"
    test_authenticated_api "Core Medical Service" "$CORE_SERVICE" "/api/patients/" "$JWT_TOKEN"
    test_authenticated_api "Exams Service" "$EXAMS_SERVICE" "/api/examenes/" "$JWT_TOKEN"
    test_authenticated_api "Diagnosis Service" "$DIAGNOSIS_SERVICE" "/api/diagnosticos/" "$JWT_TOKEN"
    test_authenticated_api "Surgery Service" "$SURGERY_SERVICE" "/api/cirugias/" "$JWT_TOKEN"

    echo ""

    # Test 4: Cross-service data consistency
    print_info "Phase 4: Cross-Service Data Consistency"
    test_patient_data "$JWT_TOKEN"

    echo ""
    echo "=========================================="
    print_success "Test suite completed!"
    echo "=========================================="
}

# Check if services are running
print_info "Checking if services are running..."

services=("$CORE_SERVICE" "$EXAMS_SERVICE" "$DIAGNOSIS_SERVICE" "$SURGERY_SERVICE")
for service in "${services[@]}"; do
    if ! curl -s -f "$service/health/live" > /dev/null; then
        print_fail "Service $service is not running. Please start all services first."
        echo ""
        echo "To start services locally:"
        echo "  1. Core Medical Service: cd services/core-medical-service && python manage.py runserver 8000"
        echo "  2. Exams Service: cd services/exams-service && python manage.py runserver 8001"
        echo "  3. Diagnosis Service: cd services/diagnosis-service && python manage.py runserver 8002"
        echo "  4. Surgery Service: cd services/surgery-service && python manage.py runserver 8003"
        exit 1
    fi
done

# Run main test suite
main
