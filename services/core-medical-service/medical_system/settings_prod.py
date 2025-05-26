from .settings import *
from google.cloud import secretmanager

# Improved secret manager access with better error handling
def access_secret_version(secret_id, version_id="latest", fallback=None):
    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/molten-avenue-460900-a0/secrets/{secret_id}/versions/{version_id}"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        print(f"Error accessing secret {secret_id}: {e}")
        return fallback

# Configuración para producción
DEBUG = True  # Set to False for production

# Cargar SECRET_KEY desde Secret Manager
SECRET_KEY = access_secret_version("jwt-secret-key", fallback=SECRET_KEY)

# Permitir hosts de Cloud Run
ALLOWED_HOSTS = ['*']

# CSRF configuration for Cloud Run
CSRF_TRUSTED_ORIGINS = [
    'https://app-medica-849622588540.us-central1.run.app',
    'https://*.run.app',
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'pacientes2',
    'consultas',
    'core',
    'storages',
]

# Middleware settings
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'medical_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'medical_system', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'medical_system.context_processors.permisos_usuario',

            ],
        },
    },
]

WSGI_APPLICATION = 'medical_system.wsgi.application'

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': access_secret_version("db-name", fallback='medical_system'),
        'USER': access_secret_version("db-user", fallback='postgres'),
        'PASSWORD': access_secret_version("db-password"),
        'HOST': '127.0.0.1',  # Para Cloud SQL Proxy local
        'PORT': '5432',
    }
}

# Si estamos en Cloud Run, usar socket para la base de datos
db_instance = access_secret_version("db-instance")
if os.environ.get('K_SERVICE') and db_instance:
    DATABASES['default']['HOST'] = f"/cloudsql/{db_instance}"
    DATABASES['default']['PORT'] = ''

# Static files settings
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Storage configuration - Django 4.2+ style (simplified for now)
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Configuración de Google Cloud Storage (disabled until secret is created)
# GOOGLE_APPLICATION_CREDENTIALS = access_secret_version("gcs-credentials-json")
# if GOOGLE_APPLICATION_CREDENTIALS:
#     os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS
#     STORAGES["default"]["BACKEND"] = "storages.backends.gcloud.GoogleCloudStorage"

# Media files settings (local for now)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Tipos de archivos permitidos
ALLOWED_FILE_EXTENSIONS = ['.jpg', '.png', '.jpeg', '.pdf', '.txt', '.dcm']



# Password validation settings
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Logging settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# Microservice URLs - Dynamic configuration for production
EXAMS_SERVICE_URL = os.getenv('EXAMS_SERVICE_URL', 'http://localhost:8001')
DIAGNOSIS_SERVICE_URL = os.getenv('DIAGNOSIS_SERVICE_URL', 'http://localhost:8002')
SURGERY_SERVICE_URL = os.getenv('SURGERY_SERVICE_URL', 'http://localhost:8003')

# REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',  # Session for web UI
        'rest_framework.authentication.BasicAuthentication',    # Basic auth for simplicity
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

# CORS settings for microservice communication
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:8001",
    "http://localhost:8002",
    "http://localhost:8003",
    "https://core-medical-service-*.run.app",
    "https://exams-service-*.run.app",
    "https://diagnosis-service-*.run.app",
    "https://surgery-service-*.run.app",
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.run\.app$",  # Allow all Cloud Run URLs
    r"^https://.*\.googleusercontent\.com$",  # Load balancer URLs
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = os.getenv('CORS_ALLOW_ALL_ORIGINS', 'False').lower() == 'true'

# Update CSRF trusted origins for production
CSRF_TRUSTED_ORIGINS = [
    "https://core-medical-service-75l2ychmxa-uc.a.run.app",
    "https://core-medical-service-43021834801.us-central1.run.app",
    "https://*.run.app",  # Allow all Cloud Run URLs
    "https://*.googleusercontent.com",  # Load balancer URLs
    "http://34.36.102.101",  # Load balancer HTTP
    "https://34.36.102.101",  # Load balancer HTTPS
    "http://localhost:8000",  # Development
]

# Security settings for production
SECURE_CROSS_ORIGIN_OPENER_POLICY = None  # Disable COOP for HTTP compatibility
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = 'DENY'

# Login/Logout URLs
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
