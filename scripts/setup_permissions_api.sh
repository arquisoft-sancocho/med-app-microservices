#!/bin/bash

# Script para configurar permisos usando el endpoint API
# Funciona con el servicio desplegado en Cloud Run

set -e

echo "=== Medical System Permissions Setup ==="
echo "Configuring groups and permissions via API endpoint..."

# Variables
SERVICE_NAME="core-medical-service"
REGION="us-central1"
PROJECT_ID="molten-avenue-460900-a0"

# Obtener la URL del servicio
echo "Getting service URL..."
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME \
  --region=$REGION \
  --format="value(status.url)" 2>/dev/null || echo "")

if [ -z "$SERVICE_URL" ]; then
    echo "Error: Service $SERVICE_NAME not found or not running"
    exit 1
fi

echo "Service URL: $SERVICE_URL"

# Token de autorización para el endpoint
AUTH_TOKEN="Bearer setup_permissions_token_2025"

# Función para hacer peticiones HTTP
make_request() {
    local endpoint=$1
    local method=${2:-GET}

    curl -s -X $method \
         -H "Authorization: $AUTH_TOKEN" \
         -H "Content-Type: application/json" \
         "$SERVICE_URL$endpoint"
}

# Verificar estado actual de permisos
echo ""
echo "Checking current permissions status..."
STATUS_RESPONSE=$(make_request "/api/permissions-status/" GET)
echo "Current status: $STATUS_RESPONSE"

# Configurar permisos
echo ""
echo "Setting up permissions..."
SETUP_RESPONSE=$(make_request "/api/setup-permissions/" POST)

# Parsear respuesta JSON (básico)
if echo "$SETUP_RESPONSE" | grep -q '"success": true'; then
    echo "✓ Permissions setup completed successfully!"
    echo ""
    echo "Response details:"
    echo "$SETUP_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$SETUP_RESPONSE"
else
    echo "✗ Error setting up permissions:"
    echo "$SETUP_RESPONSE"
    exit 1
fi

# Verificar estado final
echo ""
echo "Verifying final permissions status..."
FINAL_STATUS=$(make_request "/api/permissions-status/" GET)

if echo "$FINAL_STATUS" | grep -q '"success": true'; then
    echo "✓ Permissions verification successful!"
    echo ""
    echo "Final status:"
    echo "$FINAL_STATUS" | python3 -m json.tool 2>/dev/null || echo "$FINAL_STATUS"
else
    echo "✗ Error verifying permissions:"
    echo "$FINAL_STATUS"
fi

echo ""
echo "=== Setup Summary ==="
echo "✓ Medical system permissions configured successfully"
echo "✓ User groups created with appropriate permissions"
echo "✓ Custom permissions for medical workflows added"
echo ""
echo "Groups available:"
echo "- Administradores (System administrators)"
echo "- Medicos (Medical doctors)"
echo "- Enfermeros (Nurses)"
echo "- Recepcionistas (Receptionists)"
echo "- Tecnicos_Laboratorio (Lab technicians)"
echo "- Auditores_Medicos (Medical auditors)"
echo "- Farmaceuticos (Pharmacists)"
echo ""
echo "Access Django admin to assign users to groups:"
echo "$SERVICE_URL/admin/"
echo ""
echo "Permissions setup completed successfully!"
