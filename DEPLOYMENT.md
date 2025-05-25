# Medical Microservices Platform - GCP Deployment

[![Deploy Microservices to GCP](https://github.com/arquisoft-sancocho/med-app-microservices/actions/workflows/deploy-microservices.yml/badge.svg)](https://github.com/arquisoft-sancocho/med-app-microservices/actions/workflows/deploy-microservices.yml)

Sistema de gestión médica distribuido en microservicios desplegado en Google Cloud Platform con Load Balancer global y autoescalamient.

## 🏗️ Arquitectura

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   Frontend/     │────│  Global Load     │────│   Microservices     │
│   Mobile App    │    │  Balancer (SSL)  │    │   (Cloud Run)       │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
                              │                          │
                              │                          │
                       ┌──────▼──────┐           ┌──────▼──────┐
                       │   WAF &     │           │  Cloud SQL  │
                       │  Rate Limit │           │ (PostgreSQL)│
                       └─────────────┘           └─────────────┘
```

### Microservicios

- **Core Medical Service** (8080): Pacientes, Consultas, Autenticación
- **Exams Service** (8080): Gestión de Exámenes Médicos
- **Diagnosis Service** (8080): Gestión de Diagnósticos
- **Surgery Service** (8080): Gestión de Cirugías

### Infraestructura GCP

- **Cloud Run**: Hosting de contenedores con autoescalamiento
- **Global Load Balancer**: Distribución de tráfico con SSL automático
- **Cloud SQL**: Bases de datos PostgreSQL gestionadas
- **Artifact Registry**: Registro de imágenes Docker
- **Secret Manager**: Gestión segura de credenciales
- **Cloud Logging & Monitoring**: Observabilidad completa

## 🚀 Deployment Automatizado

### Prerequisitos

1. **Cuenta de Google Cloud Platform**
   - Proyecto configurado (`molten-avenue-460900-a0`)
   - Billing habilitado
   - APIs necesarias habilitadas

2. **Repositorio de GitHub**
   - Fork de este repositorio
   - Acceso para configurar secretos

### 1. Configuración Inicial

```bash
# Clonar el repositorio
git clone https://github.com/arquisoft-sancocho/med-app-microservices.git
cd med-app-microservices

# Verificar estado de la infraestructura
./scripts/pre-deployment-check.sh
```

### 2. Configurar Secretos de GitHub

```bash
# Generar claves y configuración
./scripts/setup-github-secrets.sh
```

**Secretos requeridos en GitHub:**

1. **GCP_SA_KEY**: Clave JSON de la Service Account
2. **JWT_SECRET_KEY**: Clave secreta para JWT

**Para agregar secretos:**
1. Ve a `Settings` → `Secrets and variables` → `Actions`
2. Click `New repository secret`
3. Agrega ambos secretos

### 3. Desplegar

```bash
# Trigger del deployment automático
./scripts/deploy-with-github-actions.sh
```

O manualmente:
```bash
git add .
git commit -m "Deploy microservices to GCP"
git push origin main
```

### 4. Monitorear Deployment

- **GitHub Actions**: [Ver progreso](https://github.com/arquisoft-sancocho/med-app-microservices/actions)
- **Cloud Run Console**: [Servicios](https://console.cloud.google.com/run)
- **Load Balancer**: [Configuración](https://console.cloud.google.com/net-services/loadbalancing)

## 🛠️ Desarrollo Local

### Docker Compose (Desarrollo)

```bash
# Iniciar todos los servicios localmente
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down
```

**URLs locales:**
- Core Medical: http://localhost:8000
- Exams Service: http://localhost:8001
- Diagnosis Service: http://localhost:8002
- Surgery Service: http://localhost:8003
- Nginx Gateway: http://localhost:80

### Testing

```bash
# Test suite completo
./scripts/test-microservices.sh

# Test individual de servicio
curl http://localhost:8000/health/ready
```

## 📋 APIs y Endpoints

### Core Medical Service
```
GET  /api/patients/          # Lista de pacientes
POST /api/patients/          # Crear paciente
GET  /api/consultations/     # Lista de consultas
POST /auth/login/            # Autenticación
GET  /health/ready           # Health check
```

### Exams Service
```
GET  /api/exams/             # Lista de exámenes
POST /api/exams/             # Crear examen
GET  /api/examenes/          # Alias en español
GET  /health/ready           # Health check
```

### Diagnosis Service
```
GET  /api/diagnosis/         # Lista de diagnósticos
POST /api/diagnosis/         # Crear diagnóstico
GET  /api/treatments/        # Tratamientos
GET  /health/ready           # Health check
```

### Surgery Service
```
GET  /api/surgeries/         # Lista de cirugías
POST /api/surgeries/         # Crear cirugía
GET  /api/cirugias/          # Alias en español
GET  /health/ready           # Health check
```

## 🔒 Seguridad

### Autenticación
- **JWT Tokens** para comunicación entre microservicios
- **Session Authentication** para interfaz web
- **Service Account** con permisos mínimos para GCP

### Red
- **HTTPS obligatorio** con certificados SSL automáticos
- **CORS configurado** para comunicación segura
- **Rate limiting** implementado en Load Balancer
- **WAF rules** para protección básica

### Datos
- **Secrets Management** con Google Secret Manager
- **Databases encriptadas** en tránsito y en reposo
- **No secrets en código** - todo en variables de entorno

## 🔧 Configuración Avanzada

### Variables de Entorno

```bash
# Configuración base
DEBUG=False
ALLOWED_HOSTS=*
DB_HOST=/cloudsql/PROJECT:REGION:INSTANCE
DB_NAME=database_name
DB_USER=postgres

# URLs de microservicios
EXAMS_SERVICE_URL=https://exams-service-xyz.run.app
DIAGNOSIS_SERVICE_URL=https://diagnosis-service-xyz.run.app
SURGERY_SERVICE_URL=https://surgery-service-xyz.run.app

# JWT Configuration
JWT_SECRET_KEY=your-secret-key
```

### Health Checks

Todos los servicios implementan:
- **Startup Probe**: `/health/ready` (inicialización)
- **Liveness Probe**: `/health/live` (disponibilidad)
- **Readiness Probe**: `/health/ready` (preparación)

### Escalamiento

```yaml
# Cloud Run configuration
min_instances: 0      # Escala a cero cuando no hay tráfico
max_instances: 10     # Máximo 10 instancias por servicio
memory: 512Mi         # 512MB RAM por instancia
cpu: 1                # 1 vCPU por instancia
```

## 📊 Monitoreo y Logs

### Cloud Logging
```bash
# Ver logs de servicio específico
gcloud logs read "resource.type=cloud_run_revision AND resource.labels.service_name=core-medical-service" --limit=50

# Logs en tiempo real
gcloud logs tail "resource.type=cloud_run_revision" --format=json
```

### Cloud Monitoring
- **Métricas de CPU y memoria** automáticas
- **Request latency y error rates**
- **Custom metrics** desde aplicaciones
- **Alertas** configurables

### Performance
```bash
# Test de carga con Apache Bench
ab -n 1000 -c 10 https://[LB-IP]/api/patients/

# Test con JMeter
# Usar archivo: Jmeter-test/Load-tests.jmx
```

## 🛡️ Troubleshooting

### Comandos Útiles

```bash
# Estado de servicios Cloud Run
gcloud run services list --region=us-central1

# Logs de deployment
gcloud builds list --limit=10

# IP del Load Balancer
gcloud compute addresses describe medical-microservices-ip --global

# Test de conectividad
curl -I https://[LB-IP]/health/ready

# Verificar SSL
openssl s_client -connect [LB-IP]:443 -servername [DOMAIN]
```

### Problemas Comunes

**1. 502 Bad Gateway**
```bash
# Verificar health checks
gcloud run services describe [SERVICE] --region=us-central1

# Verificar logs del servicio
gcloud logs read "resource.type=cloud_run_revision" --limit=10
```

**2. SSL Certificate Issues**
```bash
# Verificar estado del certificado
gcloud compute ssl-certificates list

# El certificado puede tardar hasta 60 minutos
```

**3. Database Connection Issues**
```bash
# Verificar Cloud SQL instances
gcloud sql instances list

# Test de conectividad
gcloud sql connect [INSTANCE] --user=postgres
```

## 📈 Escalamiento y Optimización

### Optimizaciones Implementadas

1. **Multi-stage Docker builds** - Imágenes más pequeñas
2. **Gunicorn con gevent workers** - Mejor concurrencia
3. **Health checks optimizados** - Detección rápida de problemas
4. **Database connection pooling** - Mejor performance
5. **Static files con WhiteNoise** - Menos latencia

### Roadmap

- [ ] **CI/CD Pipeline** con testing automatizado
- [ ] **Blue-Green Deployment** para cero downtime
- [ ] **Circuit Breakers** para resilencia
- [ ] **API Gateway** con Apigee
- [ ] **Service Mesh** con Istio
- [ ] **Monitoring** con Prometheus/Grafana

## 🤝 Contribución

1. Fork del repositorio
2. Crear feature branch (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push al branch (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📝 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👥 Autores

- **Equipo Arquisoft Sancocho** - *Desarrollo inicial*
- **Daniel Bolívar** - *Arquitectura de microservicios*

## 🙏 Agradecimientos

- Universidad de los Andes - Curso de Arquitectura de Software
- Google Cloud Platform - Infraestructura
- Django REST Framework - API development
- Docker & Kubernetes community
