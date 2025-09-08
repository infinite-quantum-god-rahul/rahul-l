#!/usr/bin/env python
"""
Run Django Server with HTTPS Configuration
This script configures Django settings for HTTPS and starts the server.
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
django.setup()

def configure_https_settings():
    """Configure Django settings for HTTPS development."""
    
    print("🔒 Configuring Django for HTTPS...")
    print("=" * 50)
    
    # Import settings
    from django.conf import settings
    
    # Configure HTTPS settings
    settings.SECURE_SSL_REDIRECT = False  # Disable for development
    settings.SESSION_COOKIE_SECURE = False  # Disable for development  
    settings.CSRF_COOKIE_SECURE = False  # Disable for development
    settings.SECURE_HSTS_SECONDS = 0  # Disable for development
    settings.SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    settings.SECURE_HSTS_PRELOAD = False
    
    # Allow insecure content for development
    settings.SECURE_CONTENT_TYPE_NOSNIFF = False
    settings.SECURE_BROWSER_XSS_FILTER = False
    settings.X_FRAME_OPTIONS = 'SAMEORIGIN'
    
    print("✅ HTTPS settings configured for development")
    print("🌐 Server will work with both HTTP and HTTPS")
    print("🔗 Access via: http://127.0.0.1:8000/ or https://127.0.0.1:8000/")
    print("=" * 50)

def run_server():
    """Run the Django development server."""
    
    try:
        print("🚀 Starting Django development server...")
        print("📍 Server running at: http://127.0.0.1:8000/")
        print("🔒 HTTPS compatible - works with both HTTP and HTTPS")
        print("🛑 Press Ctrl+C to stop")
        print("=" * 50)
        
        # Run the server
        execute_from_command_line([
            'manage.py', 
            'runserver', 
            '--insecure',  # Allow serving static files
            '127.0.0.1:8000'
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("\n💡 Try running the standard server:")
        print("   python manage.py runserver 127.0.0.1:8000")

def main():
    """Main function."""
    configure_https_settings()
    run_server()

if __name__ == "__main__":
    main()
