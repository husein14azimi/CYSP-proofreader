#!/usr/bin/env python3
"""
Build script for CYSP-proofreader
Handles packaging and distribution
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_dependencies():
    """Install required dependencies including Pillow for icon handling"""
    print("Installing dependencies...")
    try:
        # Install basic requirements first
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        # Install Pillow for icon handling
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False
    return True

def build_executable():
    """Build standalone executable using PyInstaller"""
    print("Building executable...")
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    try:
        # Build with icon and include the icon in the bundle
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name", "CYSP-proofreader",
            "--icon", "ui/resources/icon.ico",  # EXE file icon
            "--add-data", "ui/resources/icon.ico;ui/resources",  # Include icon in bundle
            "--clean",
            "main.py"
        ])
        print("Executable built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error building executable: {e}")
        return False

def create_distribution():
    """Create distribution package"""
    print("Creating distribution...")
    
    # Create distribution directory
    dist_dir = Path("dist_package")
    dist_dir.mkdir(exist_ok=True)
    
    # Copy executable
    exe_path = Path("dist/CYSP-proofreader.exe")
    if exe_path.exists():
        shutil.copy2(exe_path, dist_dir / "CYSP-proofreader.exe")
    
    # Copy documentation
    docs = ["README.md", "LICENSE"]
    for doc in docs:
        if Path(doc).exists():
            shutil.copy2(doc, dist_dir / doc)
    
    # Create version file
    version_file = dist_dir / "VERSION.txt"
    with open(version_file, "w") as f:
        f.write("CYSP-proofreader v1.0.0\n")
        f.write("Built on: " + str(Path().resolve()) + "\n")
    
    print(f"Distribution created in: {dist_dir}")
    return True

def main():
    """Main build function"""
    print("CYSP-proofreader - Build Script")
    print("=" * 50)
    
    # Install dependencies (including Pillow)
    if not install_dependencies():
        print("Failed to install dependencies")
        return False
    
    # Build executable
    if not build_executable():
        print("Failed to build executable")
        return False
    
    # Create distribution
    if not create_distribution():
        print("Failed to create distribution")
        return False
    
    print("\nBuild completed successfully!")
    print("Executable location: dist/CYSP-proofreader.exe")
    print("Distribution package: dist_package/")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)