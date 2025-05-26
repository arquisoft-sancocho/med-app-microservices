```mermaid
graph TB
    %% External Users and Clients
    subgraph "👥 External Users"
        U1[Web Browsers]
        U2[Mobile Apps]
        U3[API Clients]
    end

    %% Internet Gateway
    INET[🌐 Internet]

    %% Google Cloud Platform Infrastructure
    subgraph "☁️ Google Cloud Platform - Project: molten-avenue-460900-a0"

        %% Load Balancer Layer
        subgraph "🔀 Load Balancing & Gateway"
            LB[Google Cloud Load Balancer<br/>medical-api-gateway]
            SSL[SSL Certificate<br/>HTTPS Termination]
        end

        %% Cloud Run Services Layer
        subgraph "🚀 Cloud Run Services (us-central1)"
            subgraph "Core Service"
                CORE[core-medical-service<br/>Django Application<br/>Port: 8000<br/>URL: core-medical-service-43021834801.us-central1.run.app]
            end

            subgraph "Exams Service"
                EXAMS[exams-service<br/>FastAPI Application<br/>Port: 8080<br/>URL: exams-service-43021834801.us-central1.run.app]
            end

            subgraph "Diagnosis Service"
                DIAG[diagnosis-service<br/>Django Application<br/>Port: 8002<br/>URL: diagnosis-service-43021834801.us-central1.run.app]
            end

            subgraph "Surgery Service"
                SURG[surgery-service<br/>Django Application<br/>Port: 8003<br/>URL: surgery-service-43021834801.us-central1.run.app]
            end
        end

        %% Database Layer
        subgraph "🗄️ Cloud SQL Instances (us-central1)"
            subgraph "Core DB"
                COREDB[(core-medical-db<br/>PostgreSQL<br/>core_medical)]
            end

            subgraph "Exams DB"
                EXAMSDB[(exams-db<br/>PostgreSQL<br/>exams_db)]
            end

            subgraph "Diagnosis DB"
                DIAGDB[(diagnosis-db<br/>PostgreSQL<br/>diagnosis_db)]
            end

            subgraph "Surgery DB"
                SURGDB[(surgery-db<br/>PostgreSQL<br/>surgery_db)]
            end
        end

        %% Storage Layer
        subgraph "💾 Cloud Storage"
            GCS[medical-system-files<br/>Google Cloud Storage<br/>File uploads & documents]
        end

        %% Container Registry
        subgraph "📦 Artifact Registry"
            GAR[us-central1-docker.pkg.dev<br/>molten-avenue-460900-a0/microservices/<br/>- core-medical-service<br/>- exams-service<br/>- diagnosis-service<br/>- surgery-service]
        end

        %% Secrets Management
        subgraph "🔐 Secret Manager"
            SM[Secret Manager<br/>- DB passwords<br/>- JWT secrets<br/>- API keys]
        end

        %% Monitoring & Logging
        subgraph "📊 Operations Suite"
            LOGS[Cloud Logging<br/>Application logs]
            METRICS[Cloud Monitoring<br/>Performance metrics]
            TRACE[Cloud Trace<br/>Request tracing]
        end
    end

    %% CI/CD Pipeline
    subgraph "🔄 CI/CD Pipeline"
        GH[GitHub Repository<br/>med-app-microservices]
        GA[GitHub Actions<br/>deploy-microservices.yml]
        CB[Cloud Build<br/>Docker image building]
    end

    %% Path Routing Configuration
    subgraph "🛣️ Routing Rules"
        R1["/api/patients/* → core-medical-service"]
        R2["/api/consultations/* → core-medical-service"]
        R3["/api/examenes/* → exams-service"]
        R4["/api/diagnostics/* → diagnosis-service"]
        R5["/api/surgeries/* → surgery-service"]
        R6["/auth/* → core-medical-service"]
        R7["/admin/* → core-medical-service"]
    end

    %% Connections - User Traffic Flow
    U1 --> INET
    U2 --> INET
    U3 --> INET
    INET --> SSL
    SSL --> LB

    %% Load Balancer to Services
    LB --> CORE
    LB --> EXAMS
    LB --> DIAG
    LB --> SURG

    %% Service to Database Connections
    CORE -.->|Cloud SQL Proxy| COREDB
    EXAMS -.->|Cloud SQL Proxy| EXAMSDB
    DIAG -.->|Cloud SQL Proxy| DIAGDB
    SURG -.->|Cloud SQL Proxy| SURGDB

    %% File Storage Connections
    EXAMS -.->|File Upload/Download| GCS

    %% Secret Manager Connections
    CORE -.->|DB Password| SM
    EXAMS -.->|DB Password| SM
    DIAG -.->|DB Password| SM
    SURG -.->|DB Password| SM

    %% Monitoring Connections
    CORE -.->|Logs & Metrics| LOGS
    EXAMS -.->|Logs & Metrics| LOGS
    DIAG -.->|Logs & Metrics| LOGS
    SURG -.->|Logs & Metrics| LOGS

    %% CI/CD Flow
    GH --> GA
    GA --> CB
    CB --> GAR
    GAR --> CORE
    GAR --> EXAMS
    GAR --> DIAG
    GAR --> SURG

    %% Styling
    classDef serviceBox fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#000
    classDef dbBox fill:#f3e5f5,stroke:#4a148c,stroke-width:2px,color:#000
    classDef storageBox fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef infraBox fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000
    classDef userBox fill:#fce4ec,stroke:#880e4f,stroke-width:2px,color:#000

    class CORE,EXAMS,DIAG,SURG serviceBox
    class COREDB,EXAMSDB,DIAGDB,SURGDB dbBox
    class GCS,GAR,SM storageBox
    class LB,SSL,CB,GA infraBox
    class U1,U2,U3 userBox
```

## 📋 Diagrama de Despliegue - Sistema Médico con Microservicios

### 🏗️ **Arquitectura General**
- **Plataforma**: Google Cloud Platform (GCP)
- **Proyecto**: `molten-avenue-460900-a0`
- **Región**: `us-central1`
- **Patrón**: Microservicios con Cloud Run

### 🚀 **Servicios Desplegados**

| Servicio | Tecnología | Puerto | URL | Base de Datos |
|----------|------------|--------|-----|---------------|
| **core-medical-service** | Django | 8000 | `core-medical-service-43021834801.us-central1.run.app` | core-medical-db |
| **exams-service** | FastAPI | 8080 | `exams-service-43021834801.us-central1.run.app` | exams-db |
| **diagnosis-service** | Django | 8002 | `diagnosis-service-43021834801.us-central1.run.app` | diagnosis-db |
| **surgery-service** | Django | 8003 | `surgery-service-43021834801.us-central1.run.app` | surgery-db |

### 🔀 **Enrutamiento de Tráfico**
```
Internet → Load Balancer → Servicios Específicos
```

**Reglas de Enrutamiento:**
- `/api/patients/*` → core-medical-service
- `/api/consultations/*` → core-medical-service
- `/api/examenes/*` → exams-service
- `/api/diagnostics/*` → diagnosis-service
- `/api/surgeries/*` → surgery-service
- `/auth/*` → core-medical-service
- `/admin/*` → core-medical-service

### 🗄️ **Bases de Datos**
- **Cloud SQL PostgreSQL** para cada microservicio
- **Conexión**: Cloud SQL Proxy para seguridad
- **Respaldo**: Automatizado por GCP

### 💾 **Almacenamiento**
- **Google Cloud Storage**: `medical-system-files` (archivos médicos)
- **Artifact Registry**: Imágenes Docker de los servicios

### 🔐 **Seguridad**
- **Secret Manager**: Contraseñas y claves JWT
- **HTTPS**: Terminación SSL en Load Balancer
- **IAM**: Permisos específicos por servicio

### 🔄 **CI/CD Pipeline**
1. **GitHub**: Código fuente
2. **GitHub Actions**: Automatización del despliegue
3. **Cloud Build**: Construcción de imágenes Docker
4. **Cloud Run**: Despliegue automático

### 📊 **Monitoreo**
- **Cloud Logging**: Logs centralizados
- **Cloud Monitoring**: Métricas de rendimiento
- **Health Checks**: Endpoints `/health/ready` y `/health/live`

### 🌐 **Flujo de Datos**
1. Usuario hace petición HTTP/HTTPS
2. Load Balancer enruta según path
3. Cloud Run procesa la petición
4. Servicio consulta base de datos vía Cloud SQL Proxy
5. Si es necesario, interactúa con Cloud Storage
6. Respuesta regresa al usuario

### ⚡ **Características de Escalabilidad**
- **Auto-scaling**: 0-10 instancias por servicio
- **Load Balancing**: Distribución automática de carga
- **Stateless**: Servicios sin estado para mejor escalabilidad
- **Health Checks**: Recuperación automática ante fallos
