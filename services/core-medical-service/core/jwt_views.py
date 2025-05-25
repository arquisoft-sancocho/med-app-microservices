from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .authentication import generate_jwt_token, validate_jwt_token
import json

@api_view(['POST'])
@permission_classes([AllowAny])
def jwt_login(request):
    """
    JWT Login endpoint for microservices authentication
    """
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Username and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Authenticate user
        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Generate JWT token
        token = generate_jwt_token(user)

        return Response({
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_staff': user.is_staff,
                'groups': [group.name for group in user.groups.all()]
            }
        }, status=status.HTTP_200_OK)

    except json.JSONDecodeError:
        return Response(
            {'error': 'Invalid JSON'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def jwt_validate(request):
    """
    Validate JWT token endpoint
    """
    try:
        data = json.loads(request.body)
        token = data.get('token')

        if not token:
            return Response(
                {'error': 'Token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate token
        payload = validate_jwt_token(token)

        return Response({
            'valid': True,
            'payload': payload
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'valid': False, 'error': str(e)},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
def jwt_refresh(request):
    """
    Refresh JWT token endpoint
    """
    try:
        data = json.loads(request.body)
        token = data.get('token')

        if not token:
            return Response(
                {'error': 'Token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate current token
        payload = validate_jwt_token(token)
        user_id = payload.get('user_id')

        # Get user and generate new token
        user = User.objects.get(id=user_id)
        new_token = generate_jwt_token(user)

        return Response({
            'token': new_token
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_401_UNAUTHORIZED
        )
