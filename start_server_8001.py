#!/usr/bin/env python
"""
Start Django Server on Port 8001
Simple script to start the Django development server on the correct port.
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

def start_server():
    """Start Django server on port 8001."""
    
    print("🚀 Starting Django Server on Port 8001")
    print("=" * 50)
    print("🌐 Server will be available at: http://127.0.0.1:8001/")
    print("🔗 Access your application at: http://127.0.0.1:8001/")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Run the server on port 8001
        execute_from_command_line([
            'manage.py', 
            'runserver', 
            '--insecure',  # Allow serving static files
            '127.0.0.1:8001'
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("\n💡 Try running manually:")
        print("   python manage.py runserver 127.0.0.1:8001")

if __name__ == "__main__":
    start_server()
