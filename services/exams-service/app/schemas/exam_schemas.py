"""
Pydantic schemas for Exams Service
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from enum import Enum

# Enums
class ExamStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class ExamPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

class ResultType(str, Enum):
    NORMAL = "normal"
    ABNORMAL = "abnormal"
    INCONCLUSIVE = "inconclusive"

class AppointmentStatus(str, Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    NO_SHOW = "no_show"
    CANCELLED = "cancelled"

# Base schemas
class ExamFileBase(BaseModel):
    file_name: str
    original_name: str
    file_type: str
    file_size: int
    description: Optional[str] = None
    is_result: bool = False

class ExamFile(ExamFileBase):
    id: int
    exam_id: int
    gcs_path: str
    upload_date: datetime
    uploaded_by: int

    class Config:
        from_attributes = True

class ExamFileCreate(ExamFileBase):
    exam_id: int
    uploaded_by: int
    gcs_path: str

class ExamTypeBase(BaseModel):
    name: str = Field(..., max_length=100)
    category: str = Field(..., max_length=50)
    description: Optional[str] = None
    preparation_instructions: Optional[str] = None
    duration_minutes: int = Field(default=30, gt=0)
    cost: float = Field(default=0.0, ge=0)
    requires_fasting: bool = False
    requires_appointment: bool = True

class ExamTypeCreate(ExamTypeBase):
    pass

class ExamTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    category: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    preparation_instructions: Optional[str] = None
    duration_minutes: Optional[int] = Field(None, gt=0)
    cost: Optional[float] = Field(None, ge=0)
    requires_fasting: Optional[bool] = None
    requires_appointment: Optional[bool] = None
    is_active: Optional[bool] = None

class ExamType(ExamTypeBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Exam File schemas
class ExamFileBase(BaseModel):
    file_name: str = Field(..., max_length=255)
    original_name: str = Field(..., max_length=255)
    file_type: str = Field(..., max_length=100)
    description: Optional[str] = None
    is_result: bool = False

class ExamFileCreate(ExamFileBase):
    exam_id: int
    file_size: int
    gcs_path: str
    uploaded_by: int

class ExamFile(ExamFileBase):
    id: int
    exam_id: int
    file_size: int
    gcs_path: str
    upload_date: datetime
    uploaded_by: int

    class Config:
        from_attributes = True

# Exam schemas
class ExamBase(BaseModel):
    patient_id: int = Field(..., gt=0)
    doctor_id: int = Field(..., gt=0)
    exam_type: str = Field(..., max_length=100)
    exam_name: str = Field(..., max_length=200)
    description: Optional[str] = None
    priority: ExamPriority = ExamPriority.NORMAL
    exam_date: datetime
    notes: Optional[str] = None
    cost: float = Field(default=0.0, ge=0)

class ExamCreate(ExamBase):
    created_by: int = Field(..., gt=0)

class ExamUpdate(BaseModel):
    exam_type: Optional[str] = Field(None, max_length=100)
    exam_name: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    status: Optional[ExamStatus] = None
    priority: Optional[ExamPriority] = None
    exam_date: Optional[datetime] = None
    results: Optional[str] = None
    notes: Optional[str] = None
    cost: Optional[float] = Field(None, ge=0)
    updated_by: Optional[int] = Field(None, gt=0)

class Exam(ExamBase):
    id: int
    status: ExamStatus
    results: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: int
    updated_by: Optional[int] = None
    files: List[ExamFile] = []

    class Config:
        from_attributes = True

# Exam Result schemas
class ExamResultBase(BaseModel):
    result_type: ResultType
    findings: Optional[str] = None
    recommendations: Optional[str] = None
    reference_values: Optional[str] = None
    is_final: bool = False

class ExamResultCreate(ExamResultBase):
    exam_id: int = Field(..., gt=0)
    interpreted_by: int = Field(..., gt=0)

class ExamResultUpdate(BaseModel):
    result_type: Optional[ResultType] = None
    findings: Optional[str] = None
    recommendations: Optional[str] = None
    reference_values: Optional[str] = None
    is_final: Optional[bool] = None

class ExamResult(ExamResultBase):
    id: int
    exam_id: int
    interpreted_by: int
    interpretation_date: datetime

    class Config:
        from_attributes = True

# Exam Appointment schemas
class ExamAppointmentBase(BaseModel):
    appointment_date: datetime
    duration_minutes: int = Field(default=30, gt=0)
    location: Optional[str] = Field(None, max_length=200)
    technician_id: Optional[int] = Field(None, gt=0)
    preparation_notes: Optional[str] = None

class ExamAppointmentCreate(ExamAppointmentBase):
    exam_id: int = Field(..., gt=0)

class ExamAppointmentUpdate(BaseModel):
    appointment_date: Optional[datetime] = None
    duration_minutes: Optional[int] = Field(None, gt=0)
    location: Optional[str] = Field(None, max_length=200)
    technician_id: Optional[int] = Field(None, gt=0)
    status: Optional[AppointmentStatus] = None
    preparation_notes: Optional[str] = None

class ExamAppointment(ExamAppointmentBase):
    id: int
    exam_id: int
    status: AppointmentStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Django-compatible schemas for backward compatibility
class ExamCompatible(BaseModel):
    """Django-compatible exam schema for backward compatibility"""
    id: int
    nombre: str
    paciente_id: int
    descripcion: str
    tipo_examen: str
    fecha_examen: datetime
    resultado: Optional[str] = None
    observaciones: Optional[str] = None
    created_at: datetime
    files: List[ExamFile] = []

    class Config:
        from_attributes = True

class ExamCreateCompatible(BaseModel):
    """Django-compatible exam creation schema"""
    nombre: str
    paciente_id: int
    descripcion: str
    tipo_examen: str
    fecha_examen: datetime
    resultado: Optional[str] = None
    observaciones: Optional[str] = None

class ExamUpdateCompatible(BaseModel):
    """Django-compatible exam update schema"""
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    tipo_examen: Optional[str] = None
    fecha_examen: Optional[datetime] = None
    resultado: Optional[str] = None
    observaciones: Optional[str] = None

# Response schemas
class ExamListResponse(BaseModel):
    results: List[ExamCompatible]
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None

class ExamResponse(ExamCompatible):
    """Single exam response"""
    pass

class FileUploadResponse(BaseModel):
    file_id: int
    file_name: str
    gcs_path: str
    message: str

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    service: str = "exams-service"
    version: str = "2.0.0"

class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime
class ExamListResponse(BaseModel):
    results: List[ExamCompatible]
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None

class ExamResponse(ExamCompatible):
    """Single exam response"""
    pass

class FileUploadResponse(BaseModel):
    file_id: int
    file_name: str
    gcs_path: str
    message: str

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    service: str = "exams-service"
    version: str = "2.0.0"
