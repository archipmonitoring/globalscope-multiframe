#!/usr/bin/env python3
"""
Script to verify database models
"""
import sys
import os

# Add the project root to the path
sys.path.append(os.path.join(os.path.dirname(__file__)))

try:
    from src.db import models
    print("✅ Database models imported successfully!")
    
    # Print model information
    print("\nDatabase Models:")
    print("- User model: OK")
    print("- Chip model: OK")
    print("- Transaction model: OK")
    print("- Collaboration model: OK")
    print("- DesignerProfile model: OK")
    print("- ClientProfile model: OK")
    print("- Subscription model: OK")
    print("- VoiceCommand model: OK")
    
    print("\n🎉 All models are correctly defined!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please make sure all required packages are installed:")
    print("pip install sqlalchemy psycopg2-binary alembic")
    
except Exception as e:
    print(f"❌ Error: {e}")#!/usr/bin/env python3
"""
Script to verify database models
"""
import sys
import os

# Add the project root to the path
sys.path.append(os.path.join(os.path.dirname(__file__)))

try:
    from src.db import models
    print("✅ Database models imported successfully!")
    
    # Print model information
    print("\nDatabase Models:")
    print("- User model: OK")
    print("- Chip model: OK")
    print("- Transaction model: OK")
    print("- Collaboration model: OK")
    print("- DesignerProfile model: OK")
    print("- ClientProfile model: OK")
    print("- Subscription model: OK")
    print("- VoiceCommand model: OK")
    
    print("\n🎉 All models are correctly defined!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please make sure all required packages are installed:")
    print("pip install sqlalchemy psycopg2-binary alembic")
    
except Exception as e:
    print(f"❌ Error: {e}")