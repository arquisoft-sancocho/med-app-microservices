"""
Exam Service - Business logic for exam management
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime
import logging

from ..models.exam_models import Exam, ExamFile, ExamType, ExamResult, ExamAppointment
from ..schemas.exam_schemas import (
    ExamCreate, ExamUpdate, ExamFileCreate,
    ExamTypeCreate, ExamTypeUpdate,
    ExamResultCreate, ExamResultUpdate,
    ExamAppointmentCreate, ExamAppointmentUpdate,
    ExamCreateCompatible, ExamUpdateCompatible
)

logger = logging.getLogger(__name__)

def exam_to_compatible_response(exam: Exam) -> dict:
    """Convert SQLAlchemy Exam model to Django-compatible response"""
    return {
        "id": exam.id,
        "nombre": exam.exam_name,
        "paciente_id": exam.patient_id,
        "descripcion": exam.description,
        "tipo_examen": exam.exam_type,
        "fecha_examen": exam.exam_date,
        "resultado": exam.results,
        "observaciones": exam.notes,
        "created_at": exam.created_at,
        "files": [
            {
                "id": f.id,
                "file_name": f.file_name,
                "original_name": f.original_name,
                "file_type": f.file_type,
                "file_size": f.file_size,
                "gcs_path": f.gcs_path,
                "upload_date": f.upload_date,
                "uploaded_by": f.uploaded_by,
                "description": f.description,
                "is_result": f.is_result
            }
            for f in exam.files
        ] if exam.files else []
    }

# Exam CRUD operations
def get_exams(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    patient_id: Optional[int] = None,
    status: Optional[str] = None
) -> List[Exam]:
    """Get list of exams with optional filtering"""
    query = db.query(Exam)
    
    if patient_id:
        query = query.filter(Exam.patient_id == patient_id)
    
    if status:
        query = query.filter(Exam.status == status)
    
    return query.offset(skip).limit(limit).all()

def get_exams_count(
    db: Session,
    patient_id: Optional[int] = None,
    status: Optional[str] = None
) -> int:
    """Get total count of exams with optional filtering"""
    query = db.query(func.count(Exam.id))
    
    if patient_id:
        query = query.filter(Exam.patient_id == patient_id)
    
    if status:
        query = query.filter(Exam.status == status)
    
    return query.scalar()

def get_exam_by_id(db: Session, exam_id: int) -> Optional[Exam]:
    """Get exam by ID"""
    return db.query(Exam).filter(Exam.id == exam_id).first()

def create_exam(db: Session, exam_data: ExamCreate) -> Exam:
    """Create a new exam"""
    db_exam = Exam(
        patient_id=exam_data.patient_id,
        doctor_id=exam_data.doctor_id,
        exam_type=exam_data.exam_type,
        exam_name=exam_data.exam_name,
        description=exam_data.description,
        priority=exam_data.priority,
        exam_date=exam_data.exam_date,
        notes=exam_data.notes,
        cost=exam_data.cost,
        created_by=exam_data.created_by
    )
    
    db.add(db_exam)
    db.commit()
    db.refresh(db_exam)
    
    logger.info(f"Created exam {db_exam.id} for patient {db_exam.patient_id}")
    return db_exam

def create_exam_compatible(db: Session, exam_data: ExamCreateCompatible) -> Exam:
    """Create a new exam using Django-compatible schema"""
    db_exam = Exam(
        patient_id=exam_data.paciente_id,
        doctor_id=1,  # Default doctor ID, should be passed from request context
        exam_type=exam_data.tipo_examen,
        exam_name=exam_data.nombre,
        description=exam_data.descripcion,
        exam_date=exam_data.fecha_examen,
        results=exam_data.resultado,
        notes=exam_data.observaciones,
        created_by=1  # Default, should be passed from request context
    )
    
    db.add(db_exam)
    db.commit()
    db.refresh(db_exam)
    
    logger.info(f"Created exam {db_exam.id} for patient {db_exam.patient_id}")
    return db_exam

def update_exam_compatible(db: Session, exam_id: int, exam_data: ExamUpdateCompatible) -> Optional[Exam]:
    """Update an existing exam using Django-compatible schema"""
    db_exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not db_exam:
        return None
    
    # Map Django fields to SQLAlchemy fields
    if exam_data.nombre is not None:
        db_exam.exam_name = exam_data.nombre
    if exam_data.descripcion is not None:
        db_exam.description = exam_data.descripcion
    if exam_data.tipo_examen is not None:
        db_exam.exam_type = exam_data.tipo_examen
    if exam_data.fecha_examen is not None:
        db_exam.exam_date = exam_data.fecha_examen
    if exam_data.resultado is not None:
        db_exam.results = exam_data.resultado
    if exam_data.observaciones is not None:
        db_exam.notes = exam_data.observaciones
    
    db_exam.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_exam)
    
    logger.info(f"Updated exam {exam_id}")
    return db_exam

def delete_exam(db: Session, exam_id: int) -> bool:
    """Delete an exam"""
    db_exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not db_exam:
        return False
    
    db.delete(db_exam)
    db.commit()
    
    logger.info(f"Deleted exam {exam_id}")
    return True

# Exam File operations
def create_exam_file(
    db: Session,
    exam_id: int,
    filename: str,
    file_url: str,
    file_size: int,
    content_type: str,
    uploaded_by: int,
    description: Optional[str] = None,
    is_result: bool = False
) -> ExamFile:
    """Create a new exam file record"""
    db_file = ExamFile(
        exam_id=exam_id,
        file_name=filename,
        original_name=filename,
        file_type=content_type,
        file_size=file_size,
        gcs_path=file_url,
        uploaded_by=uploaded_by,
        description=description,
        is_result=is_result
    )
    
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    
    logger.info(f"Created file record {db_file.id} for exam {exam_id}")
    return db_file

def get_exam_file_by_id(db: Session, file_id: int) -> Optional[ExamFile]:
    """Get exam file by ID"""
    return db.query(ExamFile).filter(ExamFile.id == file_id).first()

def delete_exam_file(db: Session, file_id: int) -> bool:
    """Delete an exam file record"""
    db_file = db.query(ExamFile).filter(ExamFile.id == file_id).first()
    if not db_file:
        return False
    
    db.delete(db_file)
    db.commit()
    
    logger.info(f"Deleted file record {file_id}")
    return True

def get_files_by_exam(db: Session, exam_id: int) -> List[ExamFile]:
    """Get all files for an exam"""
    return db.query(ExamFile).filter(ExamFile.exam_id == exam_id).all()

# Exam Type operations
def get_exam_types(db: Session, skip: int = 0, limit: int = 100) -> List[ExamType]:
    """Get list of exam types"""
    return db.query(ExamType).filter(ExamType.is_active == True).offset(skip).limit(limit).all()

def get_exam_type_by_id(db: Session, type_id: int) -> Optional[ExamType]:
    """Get exam type by ID"""
    return db.query(ExamType).filter(ExamType.id == type_id).first()

def create_exam_type(db: Session, type_data: ExamTypeCreate) -> ExamType:
    """Create a new exam type"""
    db_type = ExamType(**type_data.dict())
    db.add(db_type)
    db.commit()
    db.refresh(db_type)
    
    logger.info(f"Created exam type {db_type.id}: {db_type.name}")
    return db_type

def update_exam_type(db: Session, type_id: int, type_data: ExamTypeUpdate) -> Optional[ExamType]:
    """Update an exam type"""
    db_type = db.query(ExamType).filter(ExamType.id == type_id).first()
    if not db_type:
        return None
    
    update_data = type_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_type, field, value)
    
    db.commit()
    db.refresh(db_type)
    
    logger.info(f"Updated exam type {type_id}")
    return db_type

# Exam Result operations
def create_exam_result(db: Session, result_data: ExamResultCreate) -> ExamResult:
    """Create a new exam result"""
    db_result = ExamResult(**result_data.dict())
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    
    logger.info(f"Created exam result {db_result.id} for exam {db_result.exam_id}")
    return db_result

def get_exam_results(db: Session, exam_id: int) -> List[ExamResult]:
    """Get all results for an exam"""
    return db.query(ExamResult).filter(ExamResult.exam_id == exam_id).all()

def update_exam_result(db: Session, result_id: int, result_data: ExamResultUpdate) -> Optional[ExamResult]:
    """Update an exam result"""
    db_result = db.query(ExamResult).filter(ExamResult.id == result_id).first()
    if not db_result:
        return None
    
    update_data = result_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_result, field, value)
    
    db.commit()
    db.refresh(db_result)
    
    logger.info(f"Updated exam result {result_id}")
    return db_result

# Exam Appointment operations
def create_exam_appointment(db: Session, appointment_data: ExamAppointmentCreate) -> ExamAppointment:
    """Create a new exam appointment"""
    db_appointment = ExamAppointment(**appointment_data.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    
    logger.info(f"Created appointment {db_appointment.id} for exam {db_appointment.exam_id}")
    return db_appointment

def get_exam_appointments(db: Session, exam_id: int) -> List[ExamAppointment]:
    """Get all appointments for an exam"""
    return db.query(ExamAppointment).filter(ExamAppointment.exam_id == exam_id).all()

def update_exam_appointment(db: Session, appointment_id: int, appointment_data: ExamAppointmentUpdate) -> Optional[ExamAppointment]:
    """Update an exam appointment"""
    db_appointment = db.query(ExamAppointment).filter(ExamAppointment.id == appointment_id).first()
    if not db_appointment:
        return None
    
    update_data = appointment_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_appointment, field, value)
    
    db_appointment.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_appointment)
    
    logger.info(f"Updated appointment {appointment_id}")
    return db_appointment
