"""
Database initialization script for HoloMesh Marketplace
"""
from .database import engine, Base
from . import models

def init_db():
    """Create all tables in the database."""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def drop_db():
    """Drop all tables in the database."""
    # Drop all tables
    Base.metadata.drop_all(bind=engine)
    print("Database tables dropped successfully!")

if __name__ == "__main__":
    init_db()