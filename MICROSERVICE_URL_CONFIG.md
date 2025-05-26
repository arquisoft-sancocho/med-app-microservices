# Automatic Microservice URL Configuration

This document explains how the microservice URLs are automatically configured during deployment to ensure all services can communicate with each other.

## Problem Solved

Previously, when microservices were deployed, the `core-medical-service` didn't know the URLs of the other services (`exams-service`, `diagnosis-service`, `surgery-service`). This meant that:

1. The microservices list pages would show "Service not available"
2. Users couldn't access examenes, diagnosticos, or cirugias
3. Manual intervention was required after each deployment

## Solution

The GitHub Actions workflow now automatically:

1. **Deploys all microservices** in parallel
2. **Gets the URLs** of all deployed services
3. **Updates the core-medical-service** with the correct environment variables
4. **Sets up permissions** and user groups
5. **Configures the load balancer** with all service endpoints

## How It Works

### 1. Parallel Deployment
All microservices are deployed simultaneously using a matrix strategy:

```yaml
strategy:
  matrix:
    service:
      - name: core-medical-service
      - name: exams-service
      - name: diagnosis-service
      - name: surgery-service
```

### 2. URL Discovery and Update
After deployment, a dedicated job retrieves the URLs and updates the core service:

```bash
# Get URLs from deployed services
EXAMS_URL=$(gcloud run services describe exams-service --region=$REGION --format="value(status.url)")
DIAGNOSIS_URL=$(gcloud run services describe diagnosis-service --region=$REGION --format="value(status.url)")
SURGERY_URL=$(gcloud run services describe surgery-service --region=$REGION --format="value(status.url)")

# Update core-medical-service with the URLs
gcloud run services update core-medical-service \
  --region=$REGION \
  --update-env-vars="EXAMS_SERVICE_URL=$EXAMS_URL" \
  --update-env-vars="DIAGNOSIS_SERVICE_URL=$DIAGNOSIS_URL" \
  --update-env-vars="SURGERY_SERVICE_URL=$SURGERY_URL"
```

### 3. Permissions Setup
The workflow automatically calls the permissions setup API to create user groups:

```bash
curl -X POST "$CORE_URL/api/setup-permissions/" \
  -H "Content-Type: application/json" \
  -d '{"force": true}'
```

## Environment Variables Set

The following environment variables are automatically configured:

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `EXAMS_SERVICE_URL` | URL of the exams microservice | `https://exams-service-75l2ychmxa-uc.a.run.app` |
| `DIAGNOSIS_SERVICE_URL` | URL of the diagnosis microservice | `https://diagnosis-service-75l2ychmxa-uc.a.run.app` |
| `SURGERY_SERVICE_URL` | URL of the surgery microservice | `https://surgery-service-75l2ychmxa-uc.a.run.app` |

## User Groups Created

The permissions system automatically creates these user groups:

| Group | Access Level | Permissions |
|-------|--------------|-------------|
| `Administrador` | Full access | All modules (examenes, diagnosticos, cirugias, consultas) |
| `Medico` | Full access | All modules (examenes, diagnosticos, cirugias, consultas) |
| `Medico_de_Junta` | Full access + audit | All modules + audit permissions |
| `Enfermero` | Limited access | Examenes, diagnosticos, consultas (NO cirugias) |
| `Tecnico` | Very limited | Only examenes (NO diagnosticos, cirugias, consultas) |

## Manual Commands

If you need to update URLs manually or troubleshoot:

### Update URLs
```bash
./scripts/update-microservice-urls.sh
```

### Test Integration
```bash
./scripts/test-microservice-integration.sh
```

### Setup Permissions Manually
```bash
curl -X POST "https://your-core-service-url/api/setup-permissions/" \
  -H "Content-Type: application/json" \
  -d '{"force": true}'
```

### Check Permissions Status
```bash
curl "https://your-core-service-url/api/permissions-status/"
```

## Workflow Jobs

The GitHub Actions workflow runs in this order:

1. **`build-and-deploy`** - Builds and deploys all microservices in parallel
2. **`update-microservice-urls`** - Gets URLs and updates core service
3. **`setup-permissions`** - Creates user groups and permissions
4. **`setup-load-balancer`** - Configures the load balancer

## Verification

After deployment, you can verify everything works by:

1. **Check service health**:
   ```bash
   curl https://your-core-service-url/health/ready
   ```

2. **Check microservice integration**:
   ```bash
   curl https://your-core-service-url/examenes/
   curl https://your-core-service-url/diagnosticos/
   curl https://your-core-service-url/cirugias/
   ```

3. **Check permissions**:
   ```bash
   curl https://your-core-service-url/api/permissions-status/
   ```

## Troubleshooting

### Services Not Available
If services show as "not available":

1. Check if all microservices are deployed:
   ```bash
   gcloud run services list --region=us-central1
   ```

2. Run the URL update script:
   ```bash
   ./scripts/update-microservice-urls.sh
   ```

3. Check environment variables:
   ```bash
   gcloud run services describe core-medical-service --region=us-central1
   ```

### Permissions Not Working
If users can't access certain modules:

1. Check permissions status:
   ```bash
   curl https://your-core-service-url/api/permissions-status/
   ```

2. Re-run permissions setup:
   ```bash
   curl -X POST "https://your-core-service-url/api/setup-permissions/" \
     -H "Content-Type: application/json" \
     -d '{"force": true}'
   ```

3. Assign users to groups through Django admin panel

## Benefits

✅ **Automatic Configuration** - No manual intervention required
✅ **Consistent Deployment** - Same process every time
✅ **Error Prevention** - Reduces human error
✅ **Fast Deployment** - Parallel deployment for speed
✅ **Complete Setup** - Permissions and URLs configured automatically
✅ **Easy Debugging** - Scripts available for manual testing
