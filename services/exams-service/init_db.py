#!/usr/bin/env python3
"""
Database initialization script for FastAPI Exams Service
"""
import asyncio
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import exam_models
from app.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    """Initialize database with tables"""
    try:
        # Create engine
        engine = create_engine(settings.DATABASE_URL, echo=True)

        # Create all tables
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)

        # Create session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()

        # Insert default exam types
        default_exam_types = [
            {
                "name": "Electroencefalograma",
                "category": "neurology",
                "description": "Examen de actividad eléctrica cerebral",
                "duration_minutes": 60,
                "cost": 150000.0,
                "requires_fasting": False,
                "requires_appointment": True
            },
            {
                "name": "Resonancia Magnética",
                "category": "imaging",
                "description": "Imágenes por resonancia magnética",
                "duration_minutes": 45,
                "cost": 800000.0,
                "requires_fasting": False,
                "requires_appointment": True
            },
            {
                "name": "MicroRNA",
                "category": "laboratory",
                "description": "Análisis de microRNA",
                "duration_minutes": 30,
                "cost": 200000.0,
                "requires_fasting": True,
                "requires_appointment": True
            },
            {
                "name": "Examen de Sangre",
                "category": "laboratory",
                "description": "Análisis completo de sangre",
                "duration_minutes": 15,
                "cost": 50000.0,
                "requires_fasting": True,
                "requires_appointment": False
            },
            {
                "name": "Rayos X",
                "category": "imaging",
                "description": "Radiografía",
                "duration_minutes": 15,
                "cost": 80000.0,
                "requires_fasting": False,
                "requires_appointment": False
            },
            {
                "name": "Ultrasonido",
                "category": "imaging",
                "description": "Ecografía",
                "duration_minutes": 30,
                "cost": 120000.0,
                "requires_fasting": False,
                "requires_appointment": True
            },
            {
                "name": "Tomografía",
                "category": "imaging",
                "description": "Tomografía computarizada",
                "duration_minutes": 30,
                "cost": 400000.0,
                "requires_fasting": False,
                "requires_appointment": True
            },
            {
                "name": "Laboratorio General",
                "category": "laboratory",
                "description": "Exámenes de laboratorio general",
                "duration_minutes": 20,
                "cost": 75000.0,
                "requires_fasting": True,
                "requires_appointment": False
            }
        ]

        # Check if exam types already exist
        existing_types = db.query(exam_models.ExamType).first()
        if not existing_types:
            logger.info("Inserting default exam types...")
            for exam_type_data in default_exam_types:
                exam_type = exam_models.ExamType(**exam_type_data)
                db.add(exam_type)

            db.commit()
            logger.info(f"Inserted {len(default_exam_types)} default exam types")
        else:
            logger.info("Exam types already exist, skipping insertion")

        db.close()
        logger.info("Database initialization completed successfully")

    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

if __name__ == "__main__":
    init_db()
