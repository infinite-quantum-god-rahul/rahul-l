#!/usr/bin/env bash
# Build script for Render deployment - SIMPLIFIED VERSION
# This script will be executed by Render during the build process

set -o errexit  # Exit on any error

echo "🚀 Starting SML777 Django deployment build..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if we can import Django
echo "🔍 Testing Django installation..."
python -c "import django; print(f'Django version: {django.get_version()}')"

# Test with ultra-minimal settings first
echo "🔍 Testing with ultra-minimal settings..."
export DJANGO_SETTINGS_MODULE=spoorthi_macs.settings_ultra_minimal
python manage.py check --settings=spoorthi_macs.settings_ultra_minimal

# Run database migrations with ultra-minimal settings
echo "🗄️ Running database migrations..."
python manage.py migrate --noinput --settings=spoorthi_macs.settings_ultra_minimal

# Collect static files with ultra-minimal settings
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --settings=spoorthi_macs.settings_ultra_minimal

# Final check with ultra-minimal settings
echo "🔍 Running final Django checks..."
python manage.py check --deploy --settings=spoorthi_macs.settings_ultra_minimal

echo "✅ Build completed successfully!"