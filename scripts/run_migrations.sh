#!/bin/bash
set -e

# Variables de entorno
PROJECT_ID="arquisoft-453601"
REGION="us-central1"
INSTANCE_NAME="django-db-instance"

# Realizar las migraciones
echo "Ejecutando makemigrations..."
DJANGO_SETTINGS_MODULE=medical_system.settings_prod python manage.py makemigrations

echo "Ejecutando migrate..."
# Ejecutar migraciones
DJANGO_SETTINGS_MODULE=medical_system.settings_prod python manage.py migrate

echo "Mostrando primeros 10 pacientes:"
echo "SELECT * FROM pacientes_paciente LIMIT 10;" | python manage.py dbshell
