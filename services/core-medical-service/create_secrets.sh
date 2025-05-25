#!/bin/bash

# Script to create all required secrets in Google Cloud Secret Manager
# Run this script to set up the secrets needed for the core medical service

PROJECT_ID="molten-avenue-460900-a0"

echo "🔧 Creating secrets for project: $PROJECT_ID"

# Function to create a secret if it doesn't exist
create_secret_if_not_exists() {
    local SECRET_NAME=$1
    local SECRET_VALUE=$2

    # Check if secret exists
    if gcloud secrets describe "$SECRET_NAME" --project="$PROJECT_ID" >/dev/null 2>&1; then
        echo "✅ Secret '$SECRET_NAME' already exists"
        # Update the secret value
        echo -n "$SECRET_VALUE" | gcloud secrets versions add "$SECRET_NAME" --data-file=- --project="$PROJECT_ID"
        echo "🔄 Updated secret '$SECRET_NAME'"
    else
        echo "📝 Creating secret '$SECRET_NAME'"
        echo -n "$SECRET_VALUE" | gcloud secrets create "$SECRET_NAME" --data-file=- --project="$PROJECT_ID"
        echo "✅ Created secret '$SECRET_NAME'"
    fi
}

# Generate a secure Django secret key
DJANGO_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")

echo "📋 Creating required secrets..."

# 1. Django Secret Key
create_secret_if_not_exists "django-secret-key" "$DJANGO_SECRET_KEY"

# 2. Database secrets (you need to replace these with your actual values)
echo ""
echo "🔍 For database secrets, you need to provide the actual values:"
echo "   - Database name (typically 'medical_system')"
echo "   - Database user (typically 'django_user')"
echo "   - Database password (your actual database password)"
echo "   - Database instance connection string (format: PROJECT_ID:REGION:INSTANCE_NAME)"
echo ""

# Example values - REPLACE THESE WITH YOUR ACTUAL VALUES
DB_NAME="medical_system"
DB_USER="django_user"
DB_PASSWORD="your_secure_password_here"  # CHANGE THIS!
DB_INSTANCE="molten-avenue-460900-a0:us-central1:medical-db-instance"  # CHANGE THIS!

create_secret_if_not_exists "db-name" "$DB_NAME"
create_secret_if_not_exists "db-user" "$DB_USER"
create_secret_if_not_exists "db-password" "$DB_PASSWORD"
create_secret_if_not_exists "db-instance" "$DB_INSTANCE"

# 3. GCS Credentials (optional - can be handled by workload identity)
echo ""
echo "🔍 For GCS credentials:"
echo "   If using Workload Identity (recommended), this can be empty"
echo "   Otherwise, provide the service account JSON key"

create_secret_if_not_exists "gcs-credentials-json" ""

echo ""
echo "✅ Secret creation completed!"
echo ""
echo "🚨 IMPORTANT: You need to update the following secrets with your actual values:"
echo "   - db-password: Set your actual database password"
echo "   - db-instance: Set your actual Cloud SQL instance connection string"
echo "   - gcs-credentials-json: Set service account JSON if not using Workload Identity"
echo ""
echo "📝 To update a secret manually:"
echo "   gcloud secrets versions add SECRET_NAME --data-file=- --project=$PROJECT_ID"
echo ""
echo "🔐 To grant access to Cloud Run service:"
echo "   gcloud projects add-iam-policy-binding $PROJECT_ID \\"
echo "     --member='serviceAccount:SERVICE_ACCOUNT_EMAIL' \\"
echo "     --role='roles/secretmanager.secretAccessor'"
