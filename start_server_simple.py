#!/usr/bin/env python
"""
Simple Django Server Starter
This starts the server and provides clear instructions for browser access.
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
    """Start Django server with clear instructions."""
    
    print("🚀 Starting Django Server")
    print("=" * 60)
    print("🌐 Server will be available at: http://127.0.0.1:8001/")
    print("")
    print("🔧 IMPORTANT: If your browser redirects to HTTPS automatically:")
    print("   1. Type 'thisisunsafe' in the browser window")
    print("   2. Or click 'Advanced' → 'Proceed to 127.0.0.1 (unsafe)'")
    print("   3. Or use a different browser/incognito mode")
    print("")
    print("🔗 Alternative URLs to try:")
    print("   • http://localhost:8001/")
    print("   • http://127.0.0.1:8001/")
    print("   • http://0.0.0.0:8001/")
    print("")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        # Run the server
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
