#!/usr/bin/env python3
"""
SML777 Render.com Deployment Helper Script
==========================================

This script helps you deploy your SML777 Django application to Render.com
automatically with the correct configuration.

Repository: https://github.com/infinite-quantum-god-rahul/rahul-l.git
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def print_banner():
    """Print deployment banner"""
    print("=" * 60)
    print("🚀 SML777 RENDER.COM DEPLOYMENT HELPER")
    print("=" * 60)
    print("Repository: https://github.com/infinite-quantum-god-rahul/rahul-l.git")
    print("=" * 60)

def check_git_status():
    """Check if we're in a git repository and if files are committed"""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        if result.stdout.strip():
            print("⚠️  Warning: You have uncommitted changes!")
            print("Please commit and push your changes before deploying.")
            return False
        else:
            print("✅ Git repository is clean - ready for deployment!")
            return True
    except subprocess.CalledProcessError:
        print("❌ Error: Not in a git repository or git not available")
        return False
    except FileNotFoundError:
        print("❌ Error: Git not found. Please install Git first.")
        return False

def check_deployment_files():
    """Check if all required deployment files exist"""
    required_files = [
        'build.sh',
        'runtime.txt', 
        'render.yaml',
        'requirements.txt',
        'spoorthi_macs/settings.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required deployment files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ All required deployment files are present!")
        return True

def open_render_dashboard():
    """Open Render.com dashboard in browser"""
    print("\n🌐 Opening Render.com dashboard...")
    webbrowser.open('https://dashboard.render.com')
    print("✅ Render dashboard opened in your browser!")

def print_deployment_instructions():
    """Print step-by-step deployment instructions"""
    print("\n" + "=" * 60)
    print("📋 DEPLOYMENT INSTRUCTIONS")
    print("=" * 60)
    
    instructions = [
        "1. 🌐 Go to https://render.com and sign up/login",
        "2. 🔗 Click 'New +' → 'Web Service'",
        "3. 📁 Connect your GitHub repository: infinite-quantum-god-rahul/rahul-l",
        "4. ⚙️  Configure your service:",
        "   - Name: sml777-web",
        "   - Environment: Python 3",
        "   - Build Command: chmod +x build.sh && ./build.sh",
        "   - Start Command: gunicorn spoorthi_macs.wsgi:application",
        "5. 🗄️  Add PostgreSQL database:",
        "   - Click 'New +' → 'PostgreSQL'",
        "   - Name: sml777-db",
        "6. 🔐 Set environment variables:",
        "   - SECRET_KEY: (Render will generate one)",
        "   - DEBUG: False",
        "   - ALLOWED_HOSTS: sml777.onrender.com",
        "7. 🚀 Click 'Create Web Service' and wait for deployment!",
        "",
        "🎉 Your app will be available at: https://sml777.onrender.com",
        "👤 Admin login: admin / admin123 (change immediately!)"
    ]
    
    for instruction in instructions:
        print(instruction)

def print_environment_variables():
    """Print environment variables that need to be set"""
    print("\n" + "=" * 60)
    print("🔐 ENVIRONMENT VARIABLES TO SET")
    print("=" * 60)
    
    env_vars = {
        "SECRET_KEY": "your-super-secret-key-here",
        "DEBUG": "False",
        "ALLOWED_HOSTS": "sml777.onrender.com",
        "DATABASE_URL": "(auto-provided by Render)",
        "SML_BUREAU_PROVIDER": "CIBIL (optional)",
        "RAZORPAY_KEY_ID": "your-razorpay-key (optional)",
        "RAZORPAY_KEY_SECRET": "your-razorpay-secret (optional)"
    }
    
    for key, value in env_vars.items():
        print(f"   {key}: {value}")

def main():
    """Main deployment helper function"""
    print_banner()
    
    # Check prerequisites
    print("\n🔍 Checking prerequisites...")
    
    if not check_git_status():
        print("\n❌ Please fix git issues before deploying.")
        return
    
    if not check_deployment_files():
        print("\n❌ Please ensure all deployment files are present.")
        return
    
    print("\n✅ All prerequisites met! Ready for deployment.")
    
    # Ask user what they want to do
    print("\n" + "=" * 60)
    print("🎯 WHAT WOULD YOU LIKE TO DO?")
    print("=" * 60)
    print("1. 📋 Show deployment instructions")
    print("2. 🌐 Open Render.com dashboard")
    print("3. 🔐 Show environment variables")
    print("4. 🚀 Show everything (recommended)")
    print("5. ❌ Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                print_deployment_instructions()
                break
            elif choice == '2':
                open_render_dashboard()
                break
            elif choice == '3':
                print_environment_variables()
                break
            elif choice == '4':
                print_deployment_instructions()
                print_environment_variables()
                open_render_dashboard()
                break
            elif choice == '5':
                print("👋 Goodbye! Happy deploying!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye! Happy deploying!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            break

if __name__ == "__main__":
    main()


