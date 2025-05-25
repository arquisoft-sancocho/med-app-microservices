#!/bin/bash

# Create test user script for Cloud Run
python manage.py shell << 'EOF'
from django.contrib.auth.models import User
from django.db import transaction

email = 'danielxbolivar@gmail.com'
password = '1234567890'
username = 'danielxbolivar'

try:
    with transaction.atomic():
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            print(f'User with email {email} already exists. Updating password.')
            user.set_password(password)
            user.is_superuser = True
            user.is_staff = True
            user.save()
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_superuser=True,
                is_staff=True
            )
            print(f'Successfully created superuser: {email}')

        print(f'User details:')
        print(f'  Email: {user.email}')
        print(f'  Username: {user.username}')
        print(f'  Superuser: {user.is_superuser}')
        print(f'  Staff: {user.is_staff}')

except Exception as e:
    print(f'Error creating user: {str(e)}')
EOF
