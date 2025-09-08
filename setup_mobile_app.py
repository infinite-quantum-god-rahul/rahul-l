#!/usr/bin/env python
"""
Complete Mobile App Setup and Launch Script for SML87
"""
import os
import sys
import subprocess
import time

def run_command(command, description=""):
    """Run a command and return the result"""
    print(f"\n🔧 {description}")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd="D:\\sml87\\mobile_app")
        if result.returncode == 0:
            print(f"✅ Success: {result.stdout}")
            return True, result.stdout
        else:
            print(f"❌ Error: {result.stderr}")
            return False, result.stderr
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False, str(e)

def check_flutter_installation():
    """Check if Flutter is properly installed"""
    print("🔍 Checking Flutter Installation...")
    
    success, output = run_command("flutter --version", "Checking Flutter version")
    if not success:
        print("❌ Flutter not found. Please install Flutter first.")
        return False
    
    print("✅ Flutter is installed")
    return True

def install_dependencies():
    """Install Flutter dependencies"""
    print("\n📦 Installing Dependencies...")
    
    success, output = run_command("flutter pub get", "Installing Flutter dependencies")
    if not success:
        print("❌ Failed to install dependencies")
        return False
    
    print("✅ Dependencies installed successfully")
    return True

def check_devices():
    """Check available devices"""
    print("\n📱 Checking Available Devices...")
    
    success, output = run_command("flutter devices", "Checking available devices")
    if not success:
        print("❌ Failed to check devices")
        return False
    
    print("✅ Device check completed")
    return True

def setup_android_emulator():
    """Set up Android emulator"""
    print("\n🤖 Setting up Android Emulator...")
    
    # Check if emulators exist
    success, output = run_command("flutter emulators", "Checking available emulators")
    
    if "Unable to find any emulator sources" in output:
        print("ℹ️ No emulators found. Creating one...")
        
        # Try to create a basic emulator
        print("📝 Note: You may need to manually create an emulator in Android Studio:")
        print("   1. Open Android Studio")
        print("   2. Tools → AVD Manager")
        print("   3. Create Virtual Device")
        print("   4. Choose Pixel 4 or similar")
        print("   5. Download API 33 or 34 system image")
        print("   6. Finish setup")
        
        return False
    else:
        print("✅ Emulators found")
        return True

def run_on_web():
    """Run the app on web browser"""
    print("\n🌐 Running App on Web...")
    
    success, output = run_command("flutter run -d chrome", "Launching app on Chrome")
    if success:
        print("✅ App launched on web successfully!")
        return True
    else:
        print("❌ Failed to launch on web")
        return False

def run_on_windows():
    """Run the app on Windows desktop"""
    print("\n🖥️ Running App on Windows...")
    
    success, output = run_command("flutter run -d windows", "Launching app on Windows")
    if success:
        print("✅ App launched on Windows successfully!")
        return True
    else:
        print("❌ Failed to launch on Windows")
        return False

def main():
    """Main setup function"""
    print("🚀 SML87 Mobile App Complete Setup")
    print("=" * 60)
    
    # Step 1: Check Flutter
    if not check_flutter_installation():
        return False
    
    # Step 2: Install dependencies
    if not install_dependencies():
        return False
    
    # Step 3: Check devices
    if not check_devices():
        return False
    
    # Step 4: Try to set up emulator
    emulator_available = setup_android_emulator()
    
    # Step 5: Try different platforms
    print("\n🎯 Attempting to Launch App...")
    
    # Try web first (most reliable)
    if run_on_web():
        print("\n🎉 Success! App is running on web browser.")
        print("   You can now access it at: http://localhost:8080")
        return True
    
    # Try Windows if web fails
    if run_on_windows():
        print("\n🎉 Success! App is running on Windows desktop.")
        return True
    
    # If both fail, provide guidance
    print("\n❌ Could not launch app automatically.")
    print("\n📋 Manual Steps to Try:")
    print("1. Run: flutter run -d chrome")
    print("2. Run: flutter run -d windows")
    print("3. Set up Android emulator in Android Studio")
    print("4. Connect physical Android device")
    
    return False

if __name__ == "__main__":
    print("🔧 Starting automated mobile app setup...")
    success = main()
    
    if success:
        print("\n🎉 Mobile app setup completed successfully!")
        print("   The app should now be running in your browser or desktop.")
    else:
        print("\n⚠️ Setup completed with some issues.")
        print("   Check the output above for manual steps to complete.")
    
    print("\n💡 Tips:")
    print("   - Keep this terminal open while using the app")
    print("   - Press 'r' to hot reload, 'R' to restart")
    print("   - Press 'q' to quit the app")
    
    input("\nPress Enter to continue...")

