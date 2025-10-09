#!/usr/bin/env python3
"""
Test script for database integration
"""
import sys
import os

# Add the project root to the path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from src.db.database import SessionLocal
from src.db import crud, models
from src.db.init_db import init_db
import uuid

def test_database():
    """Test database operations"""
    print("Testing database integration...")
    
    # Initialize database
    try:
        init_db()
        print("✅ Database initialization successful")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False
    
    # Create a database session
    db = SessionLocal()
    
    try:
        # Test user creation
        user = crud.create_user(
            db=db,
            username="testuser",
            email="test@example.com",
            hashed_password="hashed_password",
            role="user"
        )
        print(f"✅ User created: {user.username}")
        
        # Test chip creation
        chip = crud.create_chip(
            db=db,
            name="Test Chip",
            description="A test chip for database integration",
            price=100.0,
            royalty=5.0,
            designer="Test Designer",
            ip_blocks=3,
            serial_number=f"SN-{str(uuid.uuid4())[:8]}",
            nft_id=f"nft_{str(uuid.uuid4())[:12]}",
            zkp_protected=True,
            source_code="// Test source code",
            owner_id=user.id,
            designer_ids=["designer1", "designer2"]
        )
        print(f"✅ Chip created: {chip.name}")
        
        # Test transaction creation
        transaction = crud.create_transaction(
            db=db,
            chip_id=chip.id,
            user_id=user.id,
            price=chip.price
        )
        print(f"✅ Transaction created: {transaction.id}")
        
        # Test retrieving data
        retrieved_user = crud.get_user(db, user.id)
        print(f"✅ User retrieved: {retrieved_user.username}")
        
        retrieved_chip = crud.get_chip(db, chip.id)
        print(f"✅ Chip retrieved: {retrieved_chip.name}")
        
        chip_transactions = crud.get_transactions_by_chip(db, chip.id)
        print(f"✅ Transactions retrieved: {len(chip_transactions)}")
        
        # Test updating data
        updated_chip = crud.update_chip(db, chip.id, price=150.0)
        print(f"✅ Chip updated: New price is {updated_chip.price}")
        
        print("✅ All database tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = test_database()
    if success:
        print("\n🎉 Database integration test completed successfully!")
        exit(0)
    else:
        print("\n❌ Database integration test failed!")
        exit(1)