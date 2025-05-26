#!/usr/bin/env python
"""
URL validation script that doesn't require database connection
"""
import os
import sys

# Add the project directory to Python path
sys.path.append('/home/db/University/arquisoft/med-app-microservices/services/core-medical-service')

# Set up Django environment without database checks
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medical_system.settings')

# Override database settings to use SQLite for validation
import django
from django.conf import settings

# Temporarily override database settings
settings.DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

django.setup()

from django.urls import reverse, NoReverseMatch

def test_url_patterns():
    """Test critical URL patterns"""

    url_patterns_to_test = [
        ('examenes_redirect', [], 'Examenes Redirect'),
        ('diagnosticos_redirect', [], 'Diagnosticos Redirect'),
        ('cirugias_redirect', [], 'Cirugias Redirect'),
        ('pacienteList2', [], 'Patient List'),
        ('consultaList', [], 'Consulta List'),
        ('user_list', [], 'User List'),
        ('index', [], 'Index'),
    ]

    results = []
    errors = []

    for url_name, args, description in url_patterns_to_test:
        try:
            url = reverse(url_name, args=args)
            results.append(f"✓ {description} ({url_name}): {url}")
        except NoReverseMatch as e:
            errors.append(f"✗ {description} ({url_name}): {str(e)}")
        except Exception as e:
            errors.append(f"✗ {description} ({url_name}): Unexpected error - {str(e)}")

    print("URL Validation Results:")
    print("=" * 50)

    if results:
        print("\nSUCCESSFUL URL PATTERNS:")
        for result in results:
            print(result)

    if errors:
        print("\nFAILED URL PATTERNS:")
        for error in errors:
            print(error)
    else:
        print("\n🎉 All critical URL patterns resolved successfully!")

    print(f"\nSummary: {len(results)} successful, {len(errors)} failed")
    return len(errors) == 0

if __name__ == '__main__':
    success = test_url_patterns()
    sys.exit(0 if success else 1)
