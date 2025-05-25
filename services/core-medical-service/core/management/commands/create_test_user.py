from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction


class Command(BaseCommand):
    help = 'Create a test user with specified credentials'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='User email address')
        parser.add_argument('--password', type=str, help='User password')
        parser.add_argument('--username', type=str, help='Username (optional, defaults to email)')
        parser.add_argument('--superuser', action='store_true', help='Create as superuser')

    def handle(self, *args, **options):
        email = options.get('email') or 'danielxbolivar@gmail.com'
        password = options.get('password') or '1234567890'
        username = options.get('username') or email.split('@')[0]
        is_superuser = options.get('superuser', False)

        try:
            with transaction.atomic():
                # Check if user already exists
                if User.objects.filter(email=email).exists():
                    user = User.objects.get(email=email)
                    self.stdout.write(
                        self.style.WARNING(f'User with email {email} already exists. Updating password.')
                    )
                    user.set_password(password)
                    if is_superuser:
                        user.is_superuser = True
                        user.is_staff = True
                    user.save()
                else:
                    # Create new user
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        is_superuser=is_superuser,
                        is_staff=is_superuser
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully created user: {email}')
                    )

                self.stdout.write(
                    self.style.SUCCESS(
                        f'User details:\n'
                        f'  Email: {user.email}\n'
                        f'  Username: {user.username}\n'
                        f'  Superuser: {user.is_superuser}\n'
                        f'  Staff: {user.is_staff}'
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating user: {str(e)}')
            )
