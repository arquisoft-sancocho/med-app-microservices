#!/bin/bash

# Surgery Service Startup Script
echo "Starting Surgery Service..."

# Set environment variables for local development
export DB_HOST=34.72.73.199
export DB_PORT=5432
export DB_NAME=surgery_db
export DB_USER=postgres
export DB_PASSWORD=surgery-db-password-123
export DEBUG=True
export CORE_SERVICE_URL=http://localhost:8000
export JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production

# Start the Django development server
python manage.py runserver 0.0.0.0:8003
