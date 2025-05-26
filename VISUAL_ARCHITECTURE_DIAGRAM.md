# 🏥 Diagrama Visual - Sistema Médico con Microservicios

## 📊 Arquitectura del Sistema Completa

```
                                    🌐 INTERNET
                                         |
                              ┌─────────────────────┐
                              │     👥 USUARIOS     │
                              │                     │
                              │  💻 Web Browsers    │
                              │  📱 Mobile Apps     │
                              │  🔌 API Clients     │
                              └─────────────────────┘
                                         |
                                         ▼
                              ┌─────────────────────┐
                              │    🔒 SSL/HTTPS     │
                              │   Certificado TLS   │
                              └─────────────────────┘
                                         |
                                         ▼
                              ┌─────────────────────┐
                              │  🔀 LOAD BALANCER   │
                              │  Google Cloud LB    │
                              │  medical-api-gateway│
                              └─────────────────────┘
                                         |
                 ┌───────────────────────┼───────────────────────┐
                 |                       |                       |
                 ▼                       ▼                       ▼
    ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
    │   🏥 CORE SERVICE   │  │  🔬 EXAMS SERVICE   │  │ 🩺 DIAGNOSIS & SURG │
    │      (Django)       │  │     (FastAPI)       │  │     (Django)        │
    │   Port: 8000        │  │   Port: 8080        │  │   Port: 8002/8003   │
    │                     │  │                     │  │                     │
    │ • /api/patients/*   │  │ • /api/examenes/*   │  │ • /api/diagnostics/ │
    │ • /api/consults/*   │  │ • File Uploads      │  │ • /api/surgeries/   │
    │ • /auth/*           │  │ • Document Mgmt     │  │ • Medical Records   │
    │ • /admin/*          │  │                     │  │                     │
    └─────────────────────┘  └─────────────────────┘  └─────────────────────┘
                |                       |                       |
                ▼                       ▼                       ▼
    ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
    │  🗄️ CORE DATABASE   │  │ 🗄️ EXAMS DATABASE  │  │ 🗄️ DIAG/SURG DB    │
    │  PostgreSQL         │  │   PostgreSQL        │  │   PostgreSQL        │
    │  core_medical       │  │   exams_db          │  │   diagnosis_db      │
    │                     │  │                     │  │   surgery_db        │
    └─────────────────────┘  └─────────────────────┘  └─────────────────────┘
                                         |
                                         ▼
                              ┌─────────────────────┐
                              │  💾 CLOUD STORAGE   │
                              │ medical-system-files│
                              │                     │
                              │ • PDF Documents     │
                              │ • Medical Images    │
                              │ • Lab Reports       │
                              │ • Exam Results      │
                              └─────────────────────┘

═══════════════════════════════════════════════════════════════════════════════

                           🏗️ INFRAESTRUCTURA Y CI/CD

    ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
    │   🔐 SECRET MGR     │  │  📦 ARTIFACT REG    │  │  📊 MONITORING      │
    │                     │  │                     │  │                     │
    │ • DB Passwords      │  │ • Docker Images     │  │ • Cloud Logging     │
    │ • JWT Secrets       │  │ • Version Control   │  │ • Cloud Monitoring  │
    │ • API Keys          │  │ • Security Scanning │  │ • Cloud Trace       │
    └─────────────────────┘  └─────────────────────┘  └─────────────────────┘

═══════════════════════════════════════════════════════════════════════════════

                               🔄 CI/CD PIPELINE

    ┌─────────────────────┐         ┌─────────────────────┐         ┌─────────────────────┐
    │   📚 GITHUB REPO    │   -->   │  ⚙️ GITHUB ACTIONS  │   -->   │  🔨 CLOUD BUILD     │
    │                     │         │                     │         │                     │
    │ • Source Code       │         │ • Automated Tests   │         │ • Docker Build      │
    │ • Dockerfiles       │         │ • Security Scans    │         │ • Image Registry    │
    │ • Deploy Scripts    │         │ • Deploy Triggers   │         │ • Auto Deploy      │
    └─────────────────────┘         └─────────────────────┘         └─────────────────────┘
                                                                              |
                                                                              ▼
                                                   ┌─────────────────────┐
                                                   │  🚀 CLOUD RUN       │
                                                   │                     │
                                                   │ • Auto Scaling      │
                                                   │ • Health Checks     │
                                                   │ • Blue/Green Deploy │
                                                   └─────────────────────┘

═══════════════════════════════════════════════════════════════════════════════

                                🌍 GOOGLE CLOUD PLATFORM
                                Project: molten-avenue-460900-a0
                                Region: us-central1

    ┌───────────────────────────────────────────────────────────────────────────┐
    │                         🏗️ NETWORKING LAYER                              │
    │                                                                           │
    │  VPC Networks │ Firewalls │ Cloud NAT │ Cloud Armor │ CDN │ SSL Certs    │
    └───────────────────────────────────────────────────────────────────────────┘

    ┌───────────────────────────────────────────────────────────────────────────┐
    │                          🔒 SECURITY LAYER                               │
    │                                                                           │
    │  IAM Roles │ Service Accounts │ Private IPs │ Cloud SQL Proxy │ KMS      │
    └───────────────────────────────────────────────────────────────────────────┘

    ┌───────────────────────────────────────────────────────────────────────────┐
    │                        📈 OPERATIONAL LAYER                              │
    │                                                                           │
    │  Auto Backup │ Disaster Recovery │ Multi-Region │ Health Monitoring      │
    └───────────────────────────────────────────────────────────────────────────┘
```

## 🔄 Flujo de Datos Principal

### 1. Flujo de Petición Usuario
```
Usuario → HTTPS → Load Balancer → Route Decision → Microservicio → Database → Response
```

### 2. Flujo de Subida de Archivos
```
Usuario → Exams Service → Authentication → File Validation → Google Cloud Storage → Database Record
```

### 3. Flujo de CI/CD
```
Code Push → GitHub Actions → Tests → Cloud Build → Docker Registry → Cloud Run → Health Check
```

## 📱 Endpoints Principales

### 🏥 Core Medical Service (Puerto 8000)
- `GET/POST /api/patients/` - Gestión de pacientes
- `GET/POST /api/consultations/` - Consultas médicas
- `POST /auth/login/` - Autenticación
- `GET /admin/` - Panel administrativo

### 🔬 Exams Service (Puerto 8080)
- `GET/POST /api/examenes/` - Gestión de exámenes
- `POST /api/examenes/upload/` - Subida de archivos
- `GET /health/ready` - Health check

### 🩺 Diagnosis Service (Puerto 8002)
- `GET/POST /api/diagnostics/` - Diagnósticos médicos
- `GET /api/diagnostics/{id}/` - Diagnóstico específico

### 🔪 Surgery Service (Puerto 8003)
- `GET/POST /api/surgeries/` - Gestión de cirugías
- `GET /api/surgeries/schedule/` - Programación quirúrgica

## 🚦 Estados del Sistema

### ✅ Servicios Activos
- **Core Medical Service**: ✅ Desplegado y funcional
- **Exams Service**: ✅ Desplegado (Storage en modo local pendiente)
- **Diagnosis Service**: ✅ Desplegado y funcional
- **Surgery Service**: ✅ Desplegado y funcional

### 🔄 Pendientes
- **GCS Integration**: Activar credenciales en Exams Service
- **File Upload Testing**: Verificar workflow completo
- **GitHub Actions**: Monitorear estabilidad de timeouts

## 📊 Métricas Clave

### Performance
- **Latencia**: < 200ms por petición
- **Throughput**: 1000+ requests/minuto
- **Uptime**: 99.9% SLA target

### Recursos
- **CPU**: Auto-scaling 0-10 instancias
- **Memory**: 2GB por instancia
- **Storage**: Ilimitado via GCS

### Costos
- **Compute**: Cloud Run pay-per-use
- **Database**: Cloud SQL estándar
- **Storage**: GCS Standard class

---

## 🎯 Próximos Pasos

1. **Forzar restart del Exams Service** para activar credenciales GCS
2. **Probar upload de archivos** end-to-end
3. **Implementar monitoring avanzado** con alertas
4. **Optimizar CI/CD** para mayor estabilidad
5. **Añadir tests de integración** automatizados
