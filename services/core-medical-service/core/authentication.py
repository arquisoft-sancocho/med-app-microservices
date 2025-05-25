"""
JWT Authentication for microservices communication
"""
import jwt
import os
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import requests
import json

# JWT Secret Key - should be shared across all microservices
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-super-secret-jwt-key-change-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRY_HOURS = 24

class JWTAuthentication(BaseAuthentication):
    """
    Custom JWT authentication for microservices
    """

    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        if not auth_header:
            return None

        try:
            # Extract token from "Bearer <token>"
            prefix, token = auth_header.split(' ')
            if prefix.lower() != 'bearer':
                return None

        except ValueError:
            return None

        try:
            # Decode JWT token
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            user_id = payload.get('user_id')

            if not user_id:
                raise AuthenticationFailed('Invalid token payload')

            # Get user from database
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise AuthenticationFailed('User not found')

            return (user, token)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')


def generate_jwt_token(user):
    """
    Generate JWT token for a user
    """
    payload = {
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRY_HOURS),
        'iat': datetime.utcnow(),
    }

    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def validate_jwt_token(token):
    """
    Validate JWT token and return user data
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token has expired')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Invalid token')


class MicroserviceClient:
    """
    HTTP client for authenticated microservice communication
    """

    def __init__(self, base_url, jwt_token=None):
        self.base_url = base_url.rstrip('/')
        self.jwt_token = jwt_token

    def _get_headers(self):
        headers = {
            'Content-Type': 'application/json',
        }
        if self.jwt_token:
            headers['Authorization'] = f'Bearer {self.jwt_token}'
        return headers

    def get(self, endpoint, params=None):
        """Make GET request to microservice"""
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self._get_headers(), params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, data=None):
        """Make POST request to microservice"""
        url = f"{self.base_url}{endpoint}"
        response = requests.post(
            url,
            headers=self._get_headers(),
            data=json.dumps(data) if data else None,
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    def put(self, endpoint, data=None):
        """Make PUT request to microservice"""
        url = f"{self.base_url}{endpoint}"
        response = requests.put(
            url,
            headers=self._get_headers(),
            data=json.dumps(data) if data else None,
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint):
        """Make DELETE request to microservice"""
        url = f"{self.base_url}{endpoint}"
        response = requests.delete(url, headers=self._get_headers(), timeout=30)
        response.raise_for_status()
        return response.json()


def get_authenticated_microservice_client(service_url, user):
    """
    Get authenticated HTTP client for microservice communication
    """
    token = generate_jwt_token(user)
    return MicroserviceClient(service_url, token)
