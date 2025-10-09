#!/usr/bin/env python3
"""
Setup script for HoloMesh Marketplace
This script guides the user through the setup process for the HoloMesh Marketplace system.
"""
import sys
import os

def print_header():
    """Print the setup header"""
    print("=" * 60)
    print("HoloMesh Marketplace Setup")
    print("=" * 60)
    print("This script will guide you through setting up the HoloMesh Marketplace system.")
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\nChecking dependencies...")
    required_packages = [
        "sqlalchemy",
        "psycopg2-binary",
        "alembic",
        "fastapi",
        "uvicorn",
        "redis",
        "flask"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Please run: python install_db_deps.py")
        return False
    
    return True

def setup_database():
    """Guide user through database setup"""
    print("\n" + "=" * 40)
    print("Database Setup")
    print("=" * 40)
    
    print("1. Configure your PostgreSQL database:")
    print("   - Edit src/db/database.py to set your database connection string")
    print("   - Default: postgresql://user:password@localhost/holomesh_db")
    print()
    
    print("2. Initialize the database:")
    print("   - Run: python init_database.py")
    print()
    
    print("3. Configure Redis (optional but recommended):")
    print("   - Install Redis server")
    print("   - Default connection: localhost:6379")
    print()

def setup_web_demo():
    """Guide user through web demo setup"""
    print("\n" + "=" * 40)
    print("Web Demo Setup")
    print("=" * 40)
    
    print("1. Start the web demo server:")
    print("   - Navigate to web_demo directory")
    print("   - Run: python app.py")
    print()
    
    print("2. Access the web demo:")
    print("   - Open browser to http://localhost:5000")
    print()

def setup_development():
    """Guide user through development setup"""
    print("\n" + "=" * 40)
    print("Development Setup")
    print("=" * 40)
    
    print("1. Run tests:")
    print("   - Run: python test_database.py")
    print()
    
    print("2. Verify models:")
    print("   - Run: python verify_models.py")
    print()

def main():
    """Main setup function"""
    print_header()
    
    # Check prerequisites
    if not check_python_version():
        return 1
    
    if not check_dependencies():
        return 1
    
    # Setup guidance
    setup_database()
    setup_web_demo()
    setup_development()
    
    # Final instructions
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print("Next steps:")
    print("1. Configure your PostgreSQL database in src/db/database.py")
    print("2. Run python init_database.py to initialize the database")
    print("3. Start the web demo: cd web_demo && python app.py")
    print("4. Visit http://localhost:5000 in your browser")
    print()
    print("For detailed instructions, see the documentation files:")
    print("- DATABASE_INTEGRATION_SUMMARY.md")
    print("- HOLOMESH_MARKETPLACE_ROADMAP.md")
    print("- IMPLEMENTATION_SUMMARY.md")
    print()
    print("Enjoy your HoloMesh Marketplace system! 🚀")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())