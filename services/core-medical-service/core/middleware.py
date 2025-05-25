from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.utils.deprecation import MiddlewareMixin
import re
import logging

# Configure logging
logger = logging.getLogger(__name__)

class LoginRequiredMiddleware(MiddlewareMixin):
    """
    Middleware that requires a user to be authenticated to view any page,
    except for those listed in the explicit exempt paths.
    """
    def __init__(self, get_response=None):
        self.get_response = get_response
        # Compile a list of explicit exempt paths to check
        self.exempt_paths = [
            '/accounts/login/',       # The login page itself
            '/admin/login/',          # Admin login page
            '/health/ready',          # Health check endpoints
            '/health/live',           # Health check endpoints
            '/auth/login/',           # JWT login endpoint
            '/auth/validate/',        # JWT validation endpoint
            '/auth/refresh/',         # JWT refresh endpoint
            '/api/',                  # API endpoints for microservices
            # Add any other paths that should be accessible without login
        ]
        # Also compile patterns to match dynamic paths like password reset URLs
        self.exempt_patterns = [
            re.compile(r'^/accounts/password_reset/'),
            re.compile(r'^/accounts/reset/'),
            re.compile(r'^/admin/'),  # All admin URLs
            # Add other patterns if needed
        ]
        logger.info(f"LoginRequiredMiddleware initialized with exempt paths: {self.exempt_paths}")
        super().__init__(get_response)

    def process_request(self, request):
        # Skip middleware completely if user is authenticated
        if request.user.is_authenticated:
            return None

        # Get the current path
        current_path = request.path_info

        # DEBUGGING - Print every request path for anonymous users
        print(f"LoginRequiredMiddleware: Checking path '{current_path}'")

        # 1. Check for direct path match
        if current_path in self.exempt_paths:
            print(f"LoginRequiredMiddleware: Path '{current_path}' exempt (direct match)")
            return None

        # 2. Check for pattern match
        for pattern in self.exempt_patterns:
            if pattern.match(current_path):
                print(f"LoginRequiredMiddleware: Path '{current_path}' exempt (pattern match)")
                return None

        # 3. Special case for login - extra check for any login path
        # This is basically a "belt and suspenders" approach to guarantee login is always accessible
        if 'login' in current_path:
            print(f"LoginRequiredMiddleware: Path '{current_path}' might be login related, exempting")
            return None

        # If it's not exempt, redirect to login
        print(f"LoginRequiredMiddleware: Redirecting to login from '{current_path}'")
        return redirect_to_login(next=request.get_full_path(), login_url='/accounts/login/')
