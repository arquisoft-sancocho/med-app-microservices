# Multi-stage build for optimized core medical service
FROM python:3.11-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create and use non-root user
RUN useradd --create-home --shell /bin/bash app

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV DJANGO_SETTINGS_MODULE=medical_system.settings

# Install runtime dependencies only
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq5 \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash app

# Copy Python packages from builder
COPY --from=builder /root/.local /home/app/.local

# Set work directory
WORKDIR /app

# Copy project files
COPY --chown=app:app . /app/

# Create required directories
RUN mkdir -p /app/staticfiles /app/media \
    && chown -R app:app /app

# Switch to non-root user
USER app

# Add local Python packages to PATH
ENV PATH=/home/app/.local/bin:$PATH

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:$PORT/health/ready || exit 1

# Expose port
EXPOSE 8080

# Run gunicorn with optimized settings
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "30", "--access-logfile", "-", "--error-logfile", "-", "medical_system.wsgi:application"]
