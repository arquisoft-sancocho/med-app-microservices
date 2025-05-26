#!/bin/bash

# Medical System Permissions Setup Script
# This script sets up all necessary groups and permissions for the medical application

set -e

echo "🏥 Medical System Permissions Setup"
echo "==================================="

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: This script must be run from the project root directory"
    echo "   Please navigate to the directory containing manage.py"
    exit 1
fi

# Check if virtual environment is activated (optional but recommended)
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Warning: No virtual environment detected"
    echo "   Consider activating your virtual environment first"
    echo ""
fi

# Check Django installation
echo "🔍 Checking Django installation..."
python -c "import django; print(f'Django version: {django.get_version()}')" 2>/dev/null || {
    echo "❌ Error: Django is not installed or not accessible"
    echo "   Please install Django: pip install django"
    exit 1
}

echo "✅ Django found"
echo ""

# Run migrations first to ensure all models exist
echo "📋 Running database migrations..."
python manage.py makemigrations --dry-run --verbosity=0 > /dev/null 2>&1 && {
    echo "   Making new migrations..."
    python manage.py makemigrations
}

echo "   Applying migrations..."
python manage.py migrate --verbosity=1

echo "✅ Migrations completed"
echo ""

# Run the permissions setup script
echo "🔐 Setting up permissions and groups..."
python scripts/setup-permissions.py

echo ""
echo "📚 Usage Instructions:"
echo "====================="
echo ""
echo "1. Create a superuser (if not already done):"
echo "   python manage.py createsuperuser"
echo ""
echo "2. Assign users to groups in Django Admin:"
echo "   - Go to /admin/"
echo "   - Navigate to Users"
echo "   - Edit user and add to appropriate groups"
echo ""
echo "3. Available groups:"
echo "   • Administradores     - Full system access"
echo "   • Médicos            - Full medical access"
echo "   • Enfermeros         - Limited medical access"
echo "   • Recepcionistas     - Patient and appointment management"
echo "   • Técnicos_Laboratorio - Laboratory management"
echo "   • Auditores_Médicos  - Read-only audit access"
echo "   • Farmacéuticos      - Prescription and treatment access"
echo ""
echo "4. Test permissions in views using:"
echo "   @permission_required('app.permission_name')"
echo "   @login_required"
echo "   user.has_perm('app.permission_name')"
echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "💡 Tip: You can re-run this script safely to update permissions"
