"""
Google Cloud Storage Service for file uploads
"""
import os
import uuid
from datetime import datetime
from typing import Optional
import logging
from fastapi import UploadFile, HTTPException
from google.cloud import storage
from google.cloud.exceptions import GoogleCloudError

from ..config import settings

logger = logging.getLogger(__name__)

class CloudStorageService:
    def __init__(self):
        """Initialize Google Cloud Storage client"""
        try:
            if settings.GOOGLE_APPLICATION_CREDENTIALS:
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.GOOGLE_APPLICATION_CREDENTIALS
            
            self.client = storage.Client()
            self.bucket_name = settings.GCS_BUCKET_NAME
            self.bucket = self.client.bucket(self.bucket_name)
            
            logger.info(f"Initialized GCS client for bucket: {self.bucket_name}")
        except Exception as e:
            logger.error(f"Failed to initialize GCS client: {e}")
            raise

    def test_storage_connection(self) -> bool:
        """Test connection to Google Cloud Storage"""
        try:
            # Try to get bucket metadata
            self.bucket.reload()
            logger.info("GCS connection test successful")
            return True
        except Exception as e:
            logger.error(f"GCS connection test failed: {e}")
            raise HTTPException(status_code=503, detail="Storage service unavailable")

    def _validate_file(self, file: UploadFile) -> None:
        """Validate uploaded file"""
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file selected")
        
        if file.size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE} bytes"
            )
        
        if file.content_type not in settings.ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed types: {', '.join(settings.ALLOWED_FILE_TYPES)}"
            )

    def _generate_file_path(self, patient_id: int, exam_id: int, filename: str) -> str:
        """Generate unique file path in GCS"""
        file_extension = os.path.splitext(filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        timestamp = datetime.now().strftime("%Y/%m/%d")
        
        return f"exams/{timestamp}/patient_{patient_id}/exam_{exam_id}/{unique_filename}"

    async def upload_exam_file(
        self,
        file: UploadFile,
        exam_id: int,
        patient_id: int,
        description: Optional[str] = None
    ) -> str:
        """
        Upload file to Google Cloud Storage
        Returns the GCS path of the uploaded file
        """
        try:
            # Validate file
            self._validate_file(file)
            
            # Generate unique file path
            file_path = self._generate_file_path(patient_id, exam_id, file.filename)
            
            # Create blob
            blob = self.bucket.blob(file_path)
            
            # Set metadata
            blob.metadata = {
                "exam_id": str(exam_id),
                "patient_id": str(patient_id),
                "original_filename": file.filename,
                "content_type": file.content_type,
                "upload_timestamp": datetime.utcnow().isoformat(),
                "description": description or ""
            }
            
            # Upload file content
            file_content = await file.read()
            blob.upload_from_string(
                file_content,
                content_type=file.content_type
            )
            
            # Make blob publicly readable (optional, depends on requirements)
            # blob.make_public()
            
            logger.info(f"Uploaded file to GCS: {file_path}")
            return f"gs://{self.bucket_name}/{file_path}"
            
        except GoogleCloudError as e:
            logger.error(f"GCS upload error: {e}")
            raise HTTPException(status_code=500, detail="File upload failed")
        except Exception as e:
            logger.error(f"Unexpected error during file upload: {e}")
            raise HTTPException(status_code=500, detail="File upload failed")

    async def delete_exam_file(self, gcs_path: str) -> bool:
        """Delete file from Google Cloud Storage"""
        try:
            # Extract blob name from GCS path
            if gcs_path.startswith(f"gs://{self.bucket_name}/"):
                blob_name = gcs_path.replace(f"gs://{self.bucket_name}/", "")
            else:
                blob_name = gcs_path
            
            blob = self.bucket.blob(blob_name)
            
            # Check if blob exists
            if blob.exists():
                blob.delete()
                logger.info(f"Deleted file from GCS: {blob_name}")
                return True
            else:
                logger.warning(f"File not found in GCS: {blob_name}")
                return False
                
        except GoogleCloudError as e:
            logger.error(f"GCS delete error: {e}")
            raise HTTPException(status_code=500, detail="File deletion failed")
        except Exception as e:
            logger.error(f"Unexpected error during file deletion: {e}")
            raise HTTPException(status_code=500, detail="File deletion failed")

    def get_file_download_url(self, gcs_path: str, expiration_hours: int = 1) -> str:
        """Generate signed URL for file download"""
        try:
            # Extract blob name from GCS path
            if gcs_path.startswith(f"gs://{self.bucket_name}/"):
                blob_name = gcs_path.replace(f"gs://{self.bucket_name}/", "")
            else:
                blob_name = gcs_path
            
            blob = self.bucket.blob(blob_name)
            
            # Generate signed URL
            from datetime import timedelta
            url = blob.generate_signed_url(
                expiration=datetime.utcnow() + timedelta(hours=expiration_hours),
                method="GET"
            )
            
            logger.info(f"Generated download URL for: {blob_name}")
            return url
            
        except GoogleCloudError as e:
            logger.error(f"Error generating download URL: {e}")
            raise HTTPException(status_code=500, detail="Failed to generate download URL")

    def list_exam_files(self, exam_id: int, patient_id: Optional[int] = None) -> list:
        """List all files for a specific exam"""
        try:
            prefix = f"exams/"
            if patient_id:
                # More specific prefix if patient_id is provided
                blobs = self.bucket.list_blobs(prefix=prefix)
                exam_blobs = []
                
                for blob in blobs:
                    if blob.metadata and blob.metadata.get("exam_id") == str(exam_id):
                        if not patient_id or blob.metadata.get("patient_id") == str(patient_id):
                            exam_blobs.append({
                                "name": blob.name,
                                "size": blob.size,
                                "created": blob.time_created.isoformat() if blob.time_created else None,
                                "content_type": blob.content_type,
                                "metadata": blob.metadata,
                                "gcs_path": f"gs://{self.bucket_name}/{blob.name}"
                            })
                
                return exam_blobs
            else:
                # Less efficient but works if no patient_id
                blobs = self.bucket.list_blobs(prefix=prefix)
                exam_blobs = []
                
                for blob in blobs:
                    if blob.metadata and blob.metadata.get("exam_id") == str(exam_id):
                        exam_blobs.append({
                            "name": blob.name,
                            "size": blob.size,
                            "created": blob.time_created.isoformat() if blob.time_created else None,
                            "content_type": blob.content_type,
                            "metadata": blob.metadata,
                            "gcs_path": f"gs://{self.bucket_name}/{blob.name}"
                        })
                
                return exam_blobs
                
        except GoogleCloudError as e:
            logger.error(f"Error listing exam files: {e}")
            raise HTTPException(status_code=500, detail="Failed to list files")

# Create singleton instance
storage_service = CloudStorageService()
