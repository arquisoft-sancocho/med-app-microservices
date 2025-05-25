# Core Medical Service - Deployment Guide

## ✅ Issues Fixed

### 1. Django STORAGES Configuration Conflict
- **Problem**: Django 4.2+ had conflicting `DEFAULT_FILE_STORAGE` and `STORAGES` settings
- **Solution**: Consolidated into proper `STORAGES` configuration format
- **Files Modified**: `medical_system/settings_prod.py`

### 2. Missing Django Apps
- **Problem**: `INSTALLED_APPS` included apps that don't exist in this microservice
- **Solution**: Removed `examenes2`, `diagnosticos2`, `cirugias` from `INSTALLED_APPS`
- **Files Modified**: `medical_system/settings_prod.py`

### 3. Missing Static Directory
- **Problem**: `STATICFILES_DIRS` referenced non-existent static directory
- **Solution**: Created the missing static directory
- **Files Modified**: Created `static/` directory

### 4. CORS Configuration
- **Problem**: Missing CORS middleware and app configuration
- **Solution**: Added `corsheaders` to `INSTALLED_APPS` and middleware
- **Files Modified**: `medical_system/settings_prod.py`

## 📋 Required Secrets Setup

The following secrets need to be created in Google Cloud Secret Manager:

```bash
# Run the provided script to create secrets
./create_secrets.sh
```

### Required Secrets:
1. `django-secret-key` - Django secret key (auto-generated)
2. `db-name` - Database name (e.g., "medical_system")
3. `db-user` - Database user (e.g., "django_user")
4. `db-password` - Database password (MUST BE SET MANUALLY)
5. `db-instance` - Cloud SQL instance connection string (MUST BE SET MANUALLY)
6. `gcs-credentials-json` - GCS service account JSON (optional if using Workload Identity)

### Critical Actions Required:
1. **Set Database Password**: Update `db-password` secret with your actual database password
2. **Set Database Instance**: Update `db-instance` secret with format: `PROJECT_ID:REGION:INSTANCE_NAME`
3. **Grant Secret Access**: Ensure Cloud Run service account has `secretmanager.secretAccessor` role

## 🚀 Deployment Steps

### 1. Create Secrets
```bash
cd /path/to/core-medical-service
./create_secrets.sh
```

### 2. Update Critical Secrets
```bash
# Set database password
echo -n "YOUR_ACTUAL_DB_PASSWORD" | gcloud secrets versions add db-password --data-file=- --project=molten-avenue-460900-a0

# Set database instance connection string
echo -n "molten-avenue-460900-a0:us-central1:YOUR_DB_INSTANCE" | gcloud secrets versions add db-instance --data-file=- --project=molten-avenue-460900-a0
```

### 3. Build and Deploy
```bash
# Build Docker image
docker build -t core-medical-service .

# Tag for Google Container Registry
docker tag core-medical-service gcr.io/molten-avenue-460900-a0/core-medical-service

# Push to registry
docker push gcr.io/molten-avenue-460900-a0/core-medical-service

# Deploy to Cloud Run
gcloud run deploy core-medical-service \
  --image gcr.io/molten-avenue-460900-a0/core-medical-service \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="EXAMS_SERVICE_URL=https://exams-service-URL,DIAGNOSIS_SERVICE_URL=https://diagnosis-service-URL,SURGERY_SERVICE_URL=https://surgery-service-URL" \
  --project molten-avenue-460900-a0
```

## 🔧 Configuration Summary

### Current Architecture
- **Core Service**: Handles patients, consultations, and orchestrates microservice calls
- **API Communication**: Uses REST APIs to communicate with other microservices
- **Database**: Cloud SQL PostgreSQL
- **Storage**: Google Cloud Storage for file uploads
- **Authentication**: Session-based for web UI, configurable for API calls

### Microservice URLs
The following environment variables control microservice communication:
- `EXAMS_SERVICE_URL` - Exams microservice endpoint
- `DIAGNOSIS_SERVICE_URL` - Diagnosis microservice endpoint
- `SURGERY_SERVICE_URL` - Surgery microservice endpoint

### Key Files Modified
- `medical_system/settings_prod.py` - Production settings with fixes
- `core/microservice_client.py` - Microservice communication client
- `core/microservice_views.py` - Views for consuming microservice APIs
- `medical_system/urls.py` - Updated URL routing for API consumption
- `pacientes2/logic/paciente2_logic.py` - Updated to use microservice client

## 🧪 Testing

### Local Validation
```bash
# Test Django configuration
python validate_settings.py

# Run Django system check
python manage.py check --settings=medical_system.settings_test
```

### Production Testing
```bash
# Test with production settings (requires secrets)
python manage.py check --settings=medical_system.settings_prod

# Test microservice connectivity
python manage.py shell --settings=medical_system.settings_prod
>>> from core.microservice_client import MicroserviceClient
>>> client = MicroserviceClient()
>>> client.health_check('exams')
```

## 📊 Next Steps

1. **Deploy Database**: Ensure Cloud SQL instance is running and accessible
2. **Create Secrets**: Run the secrets creation script and update critical values
3. **Deploy Core Service**: Build and deploy the Docker container to Cloud Run
4. **Deploy Other Microservices**: Deploy exams, diagnosis, and surgery services
5. **Configure Load Balancer**: Set up URL mapping for the complete system
6. **Test End-to-End**: Verify all microservice communication works correctly

## 🔍 Troubleshooting

### Common Issues
1. **Secret Access Denied**: Ensure service account has `secretmanager.secretAccessor` role
2. **Database Connection Failed**: Verify Cloud SQL instance is running and accessible
3. **Microservice Communication Failed**: Check service URLs and authentication
4. **Static Files Not Loading**: Ensure WhiteNoise is configured and static files are collected

### Debug Commands
```bash
# Check service logs
gcloud logs read --project=molten-avenue-460900-a0 --filter="resource.type=cloud_run_revision AND resource.labels.service_name=core-medical-service"

# Test database connection
python manage.py dbshell --settings=medical_system.settings_prod

# Test secret access
gcloud secrets versions access latest --secret="django-secret-key" --project=molten-avenue-460900-a0
```
