from .settings import *
import os
import google.auth
from google.cloud import secretmanager

# Improved secret manager access with better error handling
def access_secret_version(secret_id, version_id="latest", fallback=None):
    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/arquisoft-453601/secrets/{secret_id}/versions/{version_id}"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        print(f"Error accessing secret {secret_id}: {e}")
        return fallback

# Configuración para producción
DEBUG = False  # Set to False for production

# Cargar SECRET_KEY desde Secret Manager
SECRET_KEY = access_secret_version("django-secret-key", fallback=SECRET_KEY)

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
    'pacientes2',
    'examenes2',
    'diagnosticos2',
    'cirugias',
    'consultas',
    'core',
    'storages',
]

# Middleware settings
MIDDLEWARE = [
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
            ],
        },
    },
]

WSGI_APPLICATION = 'medical_system.wsgi.application'

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': access_secret_version("db-name"),
        'USER': access_secret_version("db-user"),
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

# WhiteNoise configuration
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Media files settings
#MEDIA_URL = '/media/'
#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



# Configuración de Google Cloud Storage
GOOGLE_APPLICATION_CREDENTIALS = access_secret_version("gcs-credentials-json")

if GOOGLE_APPLICATION_CREDENTIALS:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS

# Nombre del bucket de Google Cloud Storage
GS_BUCKET_NAME = "arquisoft-453601_imagenes"

# Configuración de almacenamiento de archivos en GCS
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
GS_DEFAULT_ACL = None  # Evita que los archivos sean públicos por defecto

MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/"

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
