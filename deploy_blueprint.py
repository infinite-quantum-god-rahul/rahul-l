#!/usr/bin/env python3
"""
SML777 Blueprint Deployment to Render.com
==========================================

One-click Blueprint deployment for your SML777 Django application.
Repository: https://github.com/infinite-quantum-god-rahul/rahul-l.git
"""

import webbrowser
import subprocess
import sys
from pathlib import Path

def print_banner():
    """Print deployment banner"""
    print("=" * 60)
    print("🚀 SML777 BLUEPRINT DEPLOYMENT TO RENDER.COM")
    print("=" * 60)
    print("Repository: https://github.com/infinite-quantum-god-rahul/rahul-l.git")
    print("Blueprint: blueprint.yaml")
    print("=" * 60)

def check_blueprint_files():
    """Check if Blueprint files exist"""
    required_files = [
        'blueprint.yaml',
        'build.sh',
        'runtime.txt',
        'requirements.txt',
        'spoorthi_macs/settings.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required Blueprint files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ All required Blueprint files are present!")
        return True

def open_blueprint_dashboard():
    """Open Render Blueprint dashboard"""
    print("\n🌐 Opening Render Blueprint dashboard...")
    webbrowser.open('https://dashboard.render.com/blueprints')
    print("✅ Render Blueprint dashboard opened!")

def print_blueprint_instructions():
    """Print Blueprint deployment instructions"""
    print("\n" + "=" * 60)
    print("📋 BLUEPRINT DEPLOYMENT INSTRUCTIONS")
    print("=" * 60)
    
    instructions = [
        "1. 🌐 Go to https://render.com and sign up/login",
        "2. 🔗 Click 'New +' → 'Blueprint'",
        "3. 📁 Connect your GitHub repository: infinite-quantum-god-rahul/rahul-l",
        "4. 📄 Select Blueprint file: blueprint.yaml",
        "5. 🌿 Select branch: main",
        "6. ⚙️  Review the configuration (everything is pre-configured!)",
        "7. 🚀 Click 'Apply' or 'Deploy'",
        "8. ⏳ Wait 5-10 minutes for deployment to complete",
        "",
        "🎉 Your app will be available at: https://sml777-web.onrender.com",
        "👤 Admin login: admin / admin123 (change immediately!)",
        "🗄️ Database: PostgreSQL automatically created and connected"
    ]
    
    for instruction in instructions:
        print(instruction)

def print_blueprint_benefits():
    """Print Blueprint benefits"""
    print("\n" + "=" * 60)
    print("✨ BLUEPRINT BENEFITS")
    print("=" * 60)
    
    benefits = [
        "✅ One-click deployment - No manual configuration needed",
        "✅ Automatic database setup - PostgreSQL ready to use",
        "✅ Environment variables pre-configured and secure",
        "✅ Service connections automatically established",
        "✅ Consistent deployment every time",
        "✅ Easy updates - Just push to GitHub",
        "✅ Web service and database created together",
        "✅ All SML features enabled by default"
    ]
    
    for benefit in benefits:
        print(benefit)

def main():
    """Main Blueprint deployment function"""
    print_banner()
    
    # Check prerequisites
    print("\n🔍 Checking Blueprint prerequisites...")
    
    if not check_blueprint_files():
        print("\n❌ Please ensure all Blueprint files are present.")
        return
    
    print("\n✅ All Blueprint prerequisites met! Ready for deployment.")
    
    # Show benefits
    print_blueprint_benefits()
    
    # Show instructions
    print_blueprint_instructions()
    
    # Ask user what they want to do
    print("\n" + "=" * 60)
    print("🎯 WHAT WOULD YOU LIKE TO DO?")
    print("=" * 60)
    print("1. 🌐 Open Render Blueprint dashboard")
    print("2. 📋 Show deployment instructions again")
    print("3. ✨ Show Blueprint benefits")
    print("4. 🚀 Show everything and open dashboard")
    print("5. ❌ Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                open_blueprint_dashboard()
                break
            elif choice == '2':
                print_blueprint_instructions()
                break
            elif choice == '3':
                print_blueprint_benefits()
                break
            elif choice == '4':
                print_blueprint_benefits()
                print_blueprint_instructions()
                open_blueprint_dashboard()
                break
            elif choice == '5':
                print("👋 Goodbye! Happy deploying with Blueprint!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye! Happy deploying with Blueprint!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            break

if __name__ == "__main__":
    main()
