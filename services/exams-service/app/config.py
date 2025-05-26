"""
Configuration settings for FastAPI Exams Service
"""
import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://exams_user:exam_password@localhost:5432/exams_db"
    )

    # Google Cloud Storage
    GCS_BUCKET_NAME: str = os.getenv("GCS_BUCKET_NAME", "medical-system-files")
    GOOGLE_APPLICATION_CREDENTIALS: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")

    # Service settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    PORT: int = int(os.getenv("PORT", "8080"))

    # CORS settings
    ALLOWED_HOSTS: List[str] = os.getenv(
        "ALLOWED_HOSTS",
        "http://localhost:3000,https://core-medical-service-*.run.app"
    ).split(",")

    # Core medical service URL for integration
    CORE_SERVICE_URL: str = os.getenv("CORE_SERVICE_URL", "http://localhost:8000")

    # File upload settings
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    ALLOWED_FILE_TYPES: List[str] = [
        "application/pdf",
        "image/jpeg",
        "image/png",
        "image/jpg",
        "application/dicom"
    ]

    class Config:
        env_file = ".env"

settings = Settings()
