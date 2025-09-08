#!/usr/bin/env bash
# Build script for Render deployment
# This script will be executed by Render during the build process

set -o errexit  # Exit on any error

echo "🚀 Starting SML777 Django deployment build..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate --noinput

# Create superuser if it doesn't exist (optional)
echo "👤 Creating superuser (if needed)..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@sml777.com', 'admin123')
    print("Superuser created: admin/admin123")
else:
    print("Superuser already exists")
EOF

echo "✅ Build completed successfully!"