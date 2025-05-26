"""
Microservice client for communicating with other services.
This module handles API calls to exams, diagnosis, and surgery microservices.
"""

import requests
import logging
from django.conf import settings
from typing import Dict, List, Optional, Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class MicroserviceClient:
    """Client for communicating with other microservices"""

    def __init__(self):
        self.session = requests.Session()
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Set default timeout
        self.timeout = 10

    def _make_request(self, method: str, url: str, **kwargs) -> Optional[Dict]:
        """Make HTTP request with error handling"""
        try:
            kwargs.setdefault('timeout', self.timeout)
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Request failed to {url}: {str(e)}")
            return None

    def _get_auth_headers(self, request) -> Dict[str, str]:
        """Get authentication headers for API requests"""
        headers = {'Content-Type': 'application/json'}

        # Forward authentication if available
        if hasattr(request, 'user') and request.user.is_authenticated:
            # You could implement JWT token forwarding here
            pass

        return headers

    # Exams Service API calls
    def get_patient_exams(self, patient_id: int, request=None) -> List[Dict]:
        """Get all exams for a patient"""
        url = f"{settings.EXAMS_SERVICE_URL.rstrip('/')}/public-api/examenes/"
        headers = self._get_auth_headers(request)
        params = {'patient_id': patient_id}

        result = self._make_request('GET', url, headers=headers, params=params)
        return result.get('results', []) if result else []

    def get_exam_detail(self, exam_id: int, request=None) -> Optional[Dict]:
        """Get detailed exam information"""
        url = f"{settings.EXAMS_SERVICE_URL.rstrip('/')}/public-api/examenes/{exam_id}/"
        headers = self._get_auth_headers(request)

        return self._make_request('GET', url, headers=headers)

    def create_exam(self, exam_data: Dict, request=None) -> Optional[Dict]:
        """Create a new exam"""
        url = f"{settings.EXAMS_SERVICE_URL.rstrip('/')}/api/examenes/"
        headers = self._get_auth_headers(request)

        return self._make_request('POST', url, headers=headers, json=exam_data)

    # Diagnosis Service API calls
    def get_patient_diagnoses(self, patient_id: int, request=None) -> List[Dict]:
        """Get all diagnoses for a patient"""
        url = f"{settings.DIAGNOSIS_SERVICE_URL.rstrip('/')}/public-api/diagnosticos/"
        headers = self._get_auth_headers(request)
        params = {'patient_id': patient_id}

        result = self._make_request('GET', url, headers=headers, params=params)
        return result.get('results', []) if result else []

    def get_diagnosis_detail(self, diagnosis_id: int, request=None) -> Optional[Dict]:
        """Get detailed diagnosis information"""
        url = f"{settings.DIAGNOSIS_SERVICE_URL.rstrip('/')}/public-api/diagnosticos/{diagnosis_id}/"
        headers = self._get_auth_headers(request)

        return self._make_request('GET', url, headers=headers)

    def create_diagnosis(self, diagnosis_data: Dict, request=None) -> Optional[Dict]:
        """Create a new diagnosis"""
        url = f"{settings.DIAGNOSIS_SERVICE_URL.rstrip('/')}/api/diagnosticos/"
        headers = self._get_auth_headers(request)

        return self._make_request('POST', url, headers=headers, json=diagnosis_data)

    # Surgery Service API calls
    def get_patient_surgeries(self, patient_id: int, request=None) -> List[Dict]:
        """Get all surgeries for a patient"""
        url = f"{settings.SURGERY_SERVICE_URL.rstrip('/')}/api/public/cirugias/"
        headers = self._get_auth_headers(request)
        params = {'patient_id': patient_id}

        result = self._make_request('GET', url, headers=headers, params=params)
        return result.get('results', []) if result else []

    def get_surgery_detail(self, surgery_id: int, request=None) -> Optional[Dict]:
        """Get detailed surgery information"""
        url = f"{settings.SURGERY_SERVICE_URL.rstrip('/')}/api/public/cirugias/{surgery_id}/"
        headers = self._get_auth_headers(request)

        return self._make_request('GET', url, headers=headers)

    def create_surgery(self, surgery_data: Dict, request=None) -> Optional[Dict]:
        """Create a new surgery"""
        url = f"{settings.SURGERY_SERVICE_URL.rstrip('/')}/api/cirugias/"
        headers = self._get_auth_headers(request)

        return self._make_request('POST', url, headers=headers, json=surgery_data)

    # Health checks
    def check_service_health(self, service_url: str) -> bool:
        """Check if a microservice is healthy"""
        try:
            url = f"{service_url.rstrip('/')}/health/ready"
            response = self.session.get(url, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def get_services_status(self) -> Dict[str, bool]:
        """Get health status of all microservices"""
        return {
            'exams': self.check_service_health(settings.EXAMS_SERVICE_URL),
            'diagnosis': self.check_service_health(settings.DIAGNOSIS_SERVICE_URL),
            'surgery': self.check_service_health(settings.SURGERY_SERVICE_URL),
        }


# Global client instance
microservice_client = MicroserviceClient()
