"""
SQLAlchemy models for Exams Service
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, nullable=False, index=True)
    doctor_id = Column(Integer, nullable=False, index=True)
    exam_type = Column(String(100), nullable=False)
    exam_name = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="pending")  # pending, in_progress, completed, cancelled
    priority = Column(String(20), default="normal")  # low, normal, high, urgent
    exam_date = Column(DateTime, nullable=False)
    results = Column(Text)
    notes = Column(Text)
    cost = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False)
    updated_by = Column(Integer)

    # Relationships
    files = relationship("ExamFile", back_populates="exam", cascade="all, delete-orphan")

class ExamType(Base):
    __tablename__ = "exam_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    category = Column(String(50), nullable=False)  # laboratory, imaging, cardiology, etc.
    description = Column(Text)
    preparation_instructions = Column(Text)
    duration_minutes = Column(Integer, default=30)
    cost = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    requires_fasting = Column(Boolean, default=False)
    requires_appointment = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ExamFile(Base):
    __tablename__ = "exam_files"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    original_name = Column(String(255), nullable=False)
    file_type = Column(String(100), nullable=False)
    file_size = Column(Integer, nullable=False)
    gcs_path = Column(String(500), nullable=False)  # Path in Google Cloud Storage
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    uploaded_by = Column(Integer, nullable=False)
    description = Column(Text)
    is_result = Column(Boolean, default=False)  # True if this file contains exam results

    # Relationships
    exam = relationship("Exam", back_populates="files")

class ExamResult(Base):
    __tablename__ = "exam_results"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    result_type = Column(String(50), nullable=False)  # normal, abnormal, inconclusive
    findings = Column(Text)
    recommendations = Column(Text)
    reference_values = Column(Text)
    interpreted_by = Column(Integer, nullable=False)  # Doctor who interpreted
    interpretation_date = Column(DateTime(timezone=True), server_default=func.now())
    is_final = Column(Boolean, default=False)

    # Relationships
    exam = relationship("Exam")

class ExamAppointment(Base):
    __tablename__ = "exam_appointments"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    appointment_date = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, default=30)
    location = Column(String(200))  # Room, department, etc.
    technician_id = Column(Integer)  # Assigned technician
    status = Column(String(50), default="scheduled")  # scheduled, confirmed, in_progress, completed, no_show, cancelled
    preparation_notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    exam = relationship("Exam")
