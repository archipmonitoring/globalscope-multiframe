#!/usr/bin/env python3
"""
Database initialization script for HoloMesh Marketplace
This script initializes the PostgreSQL database with all required tables.
"""
import sys
import os

# Add the project root to the path
sys.path.append(os.path.join(os.path.dirname(__file__)))

def main():
    """Main database initialization function"""
    print("Initializing HoloMesh Marketplace Database...")
    print("=" * 50)
    
    try:
        # Import database modules
        from src.db.database import engine, Base
        from src.db import models
        
        # Create all tables
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        
        # Print table information
        print("\nCreated tables:")
        for table_name in Base.metadata.tables:
            print(f"  - {table_name}")
        
        print("\n🎉 Database initialization completed successfully!")
        print("\nNext steps:")
        print("1. Configure your PostgreSQL connection in src/db/database.py")
        print("2. Start the web demo: cd web_demo && python app.py")
        return 0
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\nPlease install the required dependencies:")
        print("Run: python install_db_deps.py")
        return 1
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        print("\nPlease check your PostgreSQL configuration and try again.")
        return 1

if __name__ == "__main__":
    sys.exit(main())