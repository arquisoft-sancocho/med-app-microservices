# FastAPI Exams Service

Microservicio FastAPI para gestión de exámenes médicos con funcionalidad de subida de archivos a Google Cloud Storage.

## Características

- **FastAPI**: Framework moderno y rápido para APIs
- **SQLAlchemy**: ORM para base de datos PostgreSQL
- **Google Cloud Storage**: Almacenamiento de archivos médicos
- **Alembic**: Migraciones de base de datos
- **Pydantic**: Validación de datos y serialización
- **Compatibilidad Django**: Mantiene compatibilidad con el sistema core

## Estructura del Proyecto

```
exams-service/
├── app/
│   ├── __init__.py
│   ├── config.py              # Configuración
│   ├── database.py            # Configuración de base de datos
│   ├── models/
│   │   ├── __init__.py
│   │   └── exam_models.py     # Modelos SQLAlchemy
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── exam_schemas.py    # Schemas Pydantic
│   └── services/
│       ├── __init__.py
│       ├── exam_service.py    # Lógica de negocio
│       └── storage_service.py # Servicio Google Cloud Storage
├── alembic/                   # Migraciones de base de datos
├── main.py                    # Aplicación FastAPI principal
├── init_db.py                 # Script de inicialización de BD
├── requirements.txt           # Dependencias
├── Dockerfile                 # Configuración Docker
├── alembic.ini               # Configuración Alembic
└── .env.example              # Variables de entorno ejemplo
```

## Instalación Local

1. **Clonar y navegar al directorio:**
```bash
cd services/exams-service
```

2. **Crear entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno:**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. **Inicializar base de datos:**
```bash
python init_db.py
```

6. **Ejecutar servidor de desarrollo:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

## Configuración de Producción

### Variables de Entorno Requeridas

- `DATABASE_URL`: URL de conexión a PostgreSQL
- `GCS_BUCKET_NAME`: Nombre del bucket de Google Cloud Storage
- `GOOGLE_APPLICATION_CREDENTIALS`: Ruta al archivo de credenciales de GCP
- `ALLOWED_HOSTS`: Lista de hosts permitidos (separados por coma)
- `MAX_FILE_SIZE`: Tamaño máximo de archivo en bytes (default: 10MB)

### Deployment en Google Cloud Run

```bash
# Construir imagen
docker build -t gcr.io/PROJECT_ID/exams-service .

# Subir imagen
docker push gcr.io/PROJECT_ID/exams-service

# Desplegar en Cloud Run
gcloud run deploy exams-service \
  --image gcr.io/PROJECT_ID/exams-service \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL="postgresql://..." \
  --set-env-vars GCS_BUCKET_NAME="medical-files" \
  --memory 1Gi \
  --cpu 1
```

## API Endpoints

### Endpoints Públicos (para comunicación entre microservicios)

- `GET /public-api/examenes/` - Listar exámenes
- `GET /public-api/examenes/{exam_id}` - Obtener examen específico

### Endpoints Principales

- `GET /api/examenes/` - Listar exámenes con paginación
- `POST /api/examenes/` - Crear nuevo examen (con archivos opcionales)
- `GET /api/examenes/{exam_id}` - Obtener examen específico
- `PUT /api/examenes/{exam_id}` - Actualizar examen
- `DELETE /api/examenes/{exam_id}` - Eliminar examen
- `DELETE /api/examenes/{exam_id}/files/{file_id}` - Eliminar archivo

### Health Checks

- `GET /health/ready` - Verificar que el servicio está listo
- `GET /health/live` - Verificar que el servicio está vivo

### Documentación

- `GET /docs` - Swagger UI (solo en modo debug)
- `GET /redoc` - ReDoc (solo en modo debug)

## Subida de Archivos

El servicio soporta subida de archivos a Google Cloud Storage con los siguientes tipos permitidos:
- PDF (`application/pdf`)
- Imágenes JPEG (`image/jpeg`, `image/jpg`)
- Imágenes PNG (`image/png`)
- DICOM (`application/dicom`)

**Ejemplo de creación de examen con archivos:**

```bash
curl -X POST "http://localhost:8080/api/examenes/" \
  -H "Content-Type: multipart/form-data" \
  -F "nombre=Radiografía de Tórax" \
  -F "paciente_id=123" \
  -F "descripcion=Examen de rutina" \
  -F "tipo_examen=rayos_x" \
  -F "fecha_examen=2024-12-01" \
  -F "files=@imagen1.jpg" \
  -F "files=@reporte.pdf"
```

## Compatibilidad con Django

El servicio mantiene compatibilidad con el sistema Django existente a través de:

- Schemas compatibles (`ExamCompatible`, `ExamCreateCompatible`, etc.)
- Endpoints que respetan el formato de respuesta Django
- Mapeo de campos Django a SQLAlchemy

## Migraciones de Base de Datos

```bash
# Crear migración
alembic revision --autogenerate -m "Descripción del cambio"

# Aplicar migraciones
alembic upgrade head

# Ver historial
alembic history
```

## Monitoreo y Logs

El servicio incluye:
- Health checks configurados
- Logging estructurado
- Métricas básicas
- Timeouts y reintentos

## Seguridad

- Validación de tipos de archivo
- Límites de tamaño de archivo
- Validación de datos con Pydantic
- CORS configurado
- Manejo seguro de credenciales

## Desarrollo

### Estructura de Datos

**Examen:**
```json
{
  "id": 1,
  "nombre": "Resonancia Magnética",
  "paciente_id": 123,
  "descripcion": "RM de cerebro",
  "tipo_examen": "rm",
  "fecha_examen": "2024-12-01T10:00:00",
  "resultado": "Normal",
  "observaciones": "Sin hallazgos",
  "created_at": "2024-11-15T08:30:00",
  "files": [
    {
      "id": 1,
      "file_name": "rm_cerebro.dcm",
      "file_type": "application/dicom",
      "file_size": 1024000,
      "gcs_path": "gs://bucket/path/file.dcm"
    }
  ]
}
```

### Testing

```bash
# Instalar dependencias de testing
pip install pytest pytest-asyncio httpx

# Ejecutar tests
pytest tests/

# Coverage
pytest --cov=app tests/
```

## Troubleshooting

### Problemas Comunes

1. **Error de conexión a base de datos:**
   - Verificar `DATABASE_URL` en `.env`
   - Asegurar que PostgreSQL esté corriendo

2. **Error de Google Cloud Storage:**
   - Verificar `GOOGLE_APPLICATION_CREDENTIALS`
   - Verificar permisos del service account

3. **Error de CORS:**
   - Verificar `ALLOWED_HOSTS` en configuración
   - Agregar dominio del frontend

### Logs

```bash
# Ver logs en Cloud Run
gcloud logs read --service=exams-service --limit=100

# Logs locales
tail -f logs/exams-service.log
```

## Migración desde Django

Para migrar datos existentes desde Django:

1. Exportar datos del modelo Django
2. Adaptar formato a SQLAlchemy
3. Usar `init_db.py` para insertar datos
4. Verificar integridad de datos

## Contribución

1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request
