# Test settings file to validate configuration without accessing secrets
from .settings import *
import os

# Override secret functions for testing
def access_secret_version(secret_id, version_id="latest", fallback=None):
    # Return dummy values for testing
    test_secrets = {
        "django-secret-key": "dummy-secret-key-for-testing",
        "db-name": "test_db",
        "db-user": "test_user",
        "db-password": "test_password",
        "db-instance": "test-instance",
        "gcs-credentials-json": None
    }
    return test_secrets.get(secret_id, fallback)

# Configuración para testing
DEBUG = True

# Use dummy secret key
SECRET_KEY = "dummy-secret-key-for-testing"

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

# Database settings - use SQLite for testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Static files settings
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Storage configuration - Django 4.2+ style
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Media files settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

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

# Microservice URLs - Dynamic configuration for production
EXAMS_SERVICE_URL = os.getenv('EXAMS_SERVICE_URL', 'http://localhost:8001')
DIAGNOSIS_SERVICE_URL = os.getenv('DIAGNOSIS_SERVICE_URL', 'http://localhost:8002')
SURGERY_SERVICE_URL = os.getenv('SURGERY_SERVICE_URL', 'http://localhost:8003')

# REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
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
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False

# Security settings
SECURE_CROSS_ORIGIN_OPENER_POLICY = None
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = 'DENY'
