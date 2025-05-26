"""
FastAPI Exams Service
Medical System - Microservice for handling medical exams with file uploads
"""

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
import os
import logging
from datetime import datetime, date

from app.database import get_db, engine
from app.models import exam_models
from app.schemas import exam_schemas
from app.services import exam_service, storage_service
from app.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
exam_models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Medical Exams Service",
    description="Microservice for managing medical exams with file upload capabilities",
    version="2.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoints
@app.get("/health/ready", tags=["Health"])
async def readiness_check():
    """Check if the service is ready to handle requests"""
    try:
        # Test database connection
        db = next(get_db())
        db.execute(text("SELECT 1"))
        db.close()

        # Test Google Cloud Storage connection (optional for local testing)
        try:
            storage_service.test_storage_connection()
            storage_status = "connected"
        except Exception as storage_e:
            logger.warning(f"Storage service unavailable (OK for local testing): {storage_e}")
            storage_status = "unavailable (local mode)"

        return {
            "status": "ready", 
            "timestamp": datetime.utcnow().isoformat(),
            "database": "connected",
            "storage": storage_status
        }
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={"status": "not ready", "error": str(e)}
        )

@app.get("/health/live", tags=["Health"])
async def liveness_check():
    """Check if the service is alive"""
    return {"status": "alive", "timestamp": datetime.utcnow().isoformat()}

# Public API endpoints (for microservice communication)
@app.get("/public-api/examenes/", response_model=exam_schemas.ExamListResponse, tags=["Public API"])
async def get_examenes_public(
    skip: int = 0,
    limit: int = 100,
    patient_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get list of exams - public endpoint for microservice communication"""
    try:
        exams = exam_service.get_exams(
            db=db,
            skip=skip,
            limit=limit,
            patient_id=patient_id
        )
        total = exam_service.get_exams_count(db=db, patient_id=patient_id)

        return exam_schemas.ExamListResponse(
            results=[exam_service.exam_to_compatible_response(exam) for exam in exams],
            count=total,
            next=None,
            previous=None
        )
    except Exception as e:
        logger.error(f"Error getting exams: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/public-api/examenes/{exam_id}", response_model=exam_schemas.ExamResponse, tags=["Public API"])
async def get_exam_public(exam_id: int, db: Session = Depends(get_db)):
    """Get exam by ID - public endpoint for microservice communication"""
    exam = exam_service.get_exam_by_id(db=db, exam_id=exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam_service.exam_to_compatible_response(exam)

# Main API endpoints
@app.get("/api/examenes/", response_model=exam_schemas.ExamListResponse, tags=["Exams"])
async def get_examenes(
    skip: int = 0,
    limit: int = 100,
    patient_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get list of exams with pagination"""
    try:
        exams = exam_service.get_exams(
            db=db,
            skip=skip,
            limit=limit,
            patient_id=patient_id
        )
        total = exam_service.get_exams_count(db=db, patient_id=patient_id)

        return exam_schemas.ExamListResponse(
            results=[exam_service.exam_to_compatible_response(exam) for exam in exams],
            count=total,
            next=None,
            previous=None
        )
    except Exception as e:
        logger.error(f"Error getting exams: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/examenes/", response_model=exam_schemas.ExamResponse, tags=["Exams"])
async def create_exam(
    nombre: str = Form(...),
    paciente_id: int = Form(...),
    descripcion: str = Form(...),
    tipo_examen: str = Form(...),
    fecha_examen: date = Form(...),
    resultado: Optional[str] = Form(None),
    observaciones: Optional[str] = Form(None),
    files: List[UploadFile] = File(default=[]),
    db: Session = Depends(get_db)
):
    """Create a new exam with optional file attachments"""
    try:
        # Validate tipo_examen
        valid_types = ["eeg", "rm", "mirna", "sangre", "rayos_x", "ultrasonido", "tomografia", "laboratorio"]
        if tipo_examen not in valid_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid exam type. Must be one of: {', '.join(valid_types)}"
            )

        # Create exam data
        exam_data = exam_schemas.ExamCreateCompatible(
            nombre=nombre,
            paciente_id=paciente_id,
            descripcion=descripcion,
            tipo_examen=tipo_examen,
            fecha_examen=fecha_examen,
            resultado=resultado,
            observaciones=observaciones
        )

        # Create exam in database
        exam = exam_service.create_exam_compatible(db=db, exam_data=exam_data)

        # Handle file uploads if any
        uploaded_files = []
        if files and len(files) > 0 and files[0].filename:  # Check if files were actually uploaded
            for file in files:
                if file.size > settings.MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=400,
                        detail=f"File {file.filename} is too large. Max size: {settings.MAX_FILE_SIZE} bytes"
                    )

                # Upload file to Google Cloud Storage
                file_url = await storage_service.upload_exam_file(
                    file=file,
                    exam_id=exam.id,
                    patient_id=paciente_id
                )

                # Save file reference in database
                file_record = exam_service.create_exam_file(
                    db=db,
                    exam_id=exam.id,
                    filename=file.filename,
                    file_url=file_url,
                    file_size=file.size,
                    content_type=file.content_type,
                    uploaded_by=1  # Default user, should come from auth
                )
                uploaded_files.append(file_record)

        # Return exam with files
        exam_response = exam_service.exam_to_compatible_response(exam)
        return exam_response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating exam: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/examenes/{exam_id}", response_model=exam_schemas.ExamResponse, tags=["Exams"])
async def get_exam(exam_id: int, db: Session = Depends(get_db)):
    """Get exam by ID"""
    exam = exam_service.get_exam_by_id(db=db, exam_id=exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam_service.exam_to_compatible_response(exam)

@app.put("/api/examenes/{exam_id}", response_model=exam_schemas.ExamResponse, tags=["Exams"])
async def update_exam(
    exam_id: int,
    nombre: str = Form(...),
    descripcion: str = Form(...),
    tipo_examen: str = Form(...),
    fecha_examen: date = Form(...),
    resultado: Optional[str] = Form(None),
    observaciones: Optional[str] = Form(None),
    files: List[UploadFile] = File(default=[]),
    db: Session = Depends(get_db)
):
    """Update an existing exam"""
    try:
        # Check if exam exists
        existing_exam = exam_service.get_exam_by_id(db=db, exam_id=exam_id)
        if not existing_exam:
            raise HTTPException(status_code=404, detail="Exam not found")

        # Validate tipo_examen
        valid_types = ["eeg", "rm", "mirna", "sangre", "rayos_x", "ultrasonido", "tomografia", "laboratorio"]
        if tipo_examen not in valid_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid exam type. Must be one of: {', '.join(valid_types)}"
            )

        # Update exam data
        exam_update = exam_schemas.ExamUpdateCompatible(
            nombre=nombre,
            descripcion=descripcion,
            tipo_examen=tipo_examen,
            fecha_examen=fecha_examen,
            resultado=resultado,
            observaciones=observaciones
        )

        # Update exam in database
        exam = exam_service.update_exam_compatible(db=db, exam_id=exam_id, exam_data=exam_update)

        # Handle new file uploads if any
        if files and len(files) > 0 and files[0].filename:
            for file in files:
                if file.size > settings.MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=400,
                        detail=f"File {file.filename} is too large. Max size: {settings.MAX_FILE_SIZE} bytes"
                    )

                # Upload file to Google Cloud Storage
                file_url = await storage_service.upload_exam_file(
                    file=file,
                    exam_id=exam.id,
                    patient_id=exam.patient_id
                )

                # Save file reference in database
                exam_service.create_exam_file(
                    db=db,
                    exam_id=exam.id,
                    filename=file.filename,
                    file_url=file_url,
                    file_size=file.size,
                    content_type=file.content_type,
                    uploaded_by=1  # Default user, should come from auth
                )

        # Return updated exam
        exam_response = exam_service.exam_to_compatible_response(exam)
        return exam_response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating exam: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/api/examenes/{exam_id}", tags=["Exams"])
async def delete_exam(exam_id: int, db: Session = Depends(get_db)):
    """Delete an exam and its associated files"""
    try:
        # Check if exam exists
        exam = exam_service.get_exam_by_id(db=db, exam_id=exam_id)
        if not exam:
            raise HTTPException(status_code=404, detail="Exam not found")

        # Delete files from Google Cloud Storage
        if exam.files:
            for file_record in exam.files:
                await storage_service.delete_exam_file(file_record.file_url)

        # Delete exam from database (this will cascade delete files)
        exam_service.delete_exam(db=db, exam_id=exam_id)

        return {"message": "Exam deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting exam: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/api/examenes/{exam_id}/files/{file_id}", tags=["Exams"])
async def delete_exam_file(exam_id: int, file_id: int, db: Session = Depends(get_db)):
    """Delete a specific file from an exam"""
    try:
        # Check if exam exists
        exam = exam_service.get_exam_by_id(db=db, exam_id=exam_id)
        if not exam:
            raise HTTPException(status_code=404, detail="Exam not found")

        # Get file record
        file_record = exam_service.get_exam_file_by_id(db=db, file_id=file_id)
        if not file_record or file_record.exam_id != exam_id:
            raise HTTPException(status_code=404, detail="File not found")

        # Delete file from Google Cloud Storage
        await storage_service.delete_exam_file(file_record.file_url)

        # Delete file record from database
        exam_service.delete_exam_file(db=db, file_id=file_id)

        return {"message": "File deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting file: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Root endpoint
@app.get("/", tags=["Info"])
async def root():
    """Root endpoint with service information"""
    return {
        "service": "Medical Exams Service",
        "version": "2.0.0",
        "description": "FastAPI-based microservice for managing medical exams with file uploads",
        "features": [
            "Medical exam management",
            "File upload to Google Cloud Storage",
            "Patient integration",
            "RESTful API",
            "Health checks"
        ],
        "endpoints": {
            "health": "/health/ready",
            "docs": "/docs" if settings.DEBUG else "disabled in production",
            "api": "/api/examenes/"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
