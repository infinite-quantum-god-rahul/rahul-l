#!/usr/bin/env python3
"""
SML777 Quick Deploy to Render.com
=================================

One-click deployment helper for your SML777 Django application.
Repository: https://github.com/infinite-quantum-god-rahul/rahul-l.git
"""

import webbrowser
import subprocess
import sys
from pathlib import Path

def main():
    print("🚀 SML777 QUICK DEPLOY TO RENDER.COM")
    print("=" * 50)
    print("Repository: https://github.com/infinite-quantum-god-rahul/rahul-l.git")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path('manage.py').exists():
        print("❌ Error: manage.py not found. Please run this from your Django project root.")
        return
    
    print("✅ Django project detected!")
    
    # Open Render dashboard
    print("\n🌐 Opening Render.com dashboard...")
    webbrowser.open('https://dashboard.render.com')
    
    print("\n📋 QUICK DEPLOYMENT STEPS:")
    print("1. Click 'New +' → 'Web Service'")
    print("2. Connect repository: infinite-quantum-god-rahul/rahul-l")
    print("3. Use these settings:")
    print("   - Build Command: chmod +x build.sh && ./build.sh")
    print("   - Start Command: gunicorn spoorthi_macs.wsgi:application")
    print("4. Add PostgreSQL database")
    print("5. Set environment variables (see below)")
    print("6. Deploy!")
    
    print("\n🔐 REQUIRED ENVIRONMENT VARIABLES:")
    print("SECRET_KEY=your-secret-key-here")
    print("DEBUG=False")
    print("ALLOWED_HOSTS=sml777.onrender.com")
    
    print("\n🎉 After deployment:")
    print("URL: https://sml777.onrender.com")
    print("Admin: admin / admin123")
    
    print("\n✅ Render dashboard opened! Follow the steps above.")

if __name__ == "__main__":
    main()


