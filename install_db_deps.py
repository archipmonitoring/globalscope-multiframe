#!/usr/bin/env python3
"""
Script to install database dependencies for HoloMesh Marketplace
"""
import subprocess
import sys
import os

def install_package(package):
    """Install a Python package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def main():
    """Main installation function"""
    print("Installing database dependencies for HoloMesh Marketplace...")
    print("=" * 60)
    
    # List of required packages
    packages = [
        "sqlalchemy==2.0.21",
        "psycopg2-binary==2.9.7",
        "alembic==1.12.0"
    ]
    
    # Install each package
    success_count = 0
    for package in packages:
        print(f"\nInstalling {package}...")
        if install_package(package):
            success_count += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("INSTALLATION SUMMARY")
    print("=" * 60)
    print(f"Successfully installed: {success_count}/{len(packages)} packages")
    
    if success_count == len(packages):
        print("\n🎉 All database dependencies installed successfully!")
        print("\nNext steps:")
        print("1. Configure your PostgreSQL database connection in src/db/database.py")
        print("2. Run the database initialization script: python -m src.db.init_db")
        print("3. Start the web demo: cd web_demo && python app.py")
        return 0
    else:
        print(f"\n❌ {len(packages) - success_count} package(s) failed to install.")
        print("Please check your internet connection and try again.")
        return 1

if __name__ == "__main__":
    sys.exit(main())