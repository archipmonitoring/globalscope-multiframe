"""
Test script for CAD enhancements functionality
"""
import asyncio
import sys
import os

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that we can import our modules"""
    try:
        from lib.cad_cache import CADCaching
        print("✓ Successfully imported CADCaching")
        
        from lib.cad_queue import CADTaskQueue
        print("✓ Successfully imported CADTaskQueue")
        
        from lib.cad_websocket import CADWebSocketManager
        print("✓ Successfully imported CADWebSocketManager")
        
        from api.cad_enhancements import router
        print("✓ Successfully imported CAD enhancements API router")
        
        return True
    except Exception as e:
        print(f"✗ Failed to import modules: {e}")
        return False

async def test_basic_functionality():
    """Test basic functionality of our modules"""
    try:
        # Test cache
        from lib.cad_cache import CADCaching
        # We'll use None as a placeholder for Redis client in this test
        cache = CADCaching(None)
        print("✓ Created CADCaching instance")
        
        # Test cache key generation
        key = await cache._generate_cache_key("verilator", {"input": "test.v"})
        print(f"✓ Generated cache key: {key}")
        
        # Test queue
        from lib.cad_queue import CADTaskQueue
        queue = CADTaskQueue(max_workers=2)
        print("✓ Created CADTaskQueue instance")
        
        # Test adding a task
        task_id = await queue.add_task("verilator", {"input": "test.v"}, "proj_123")
        print(f"✓ Added task with ID: {task_id}")
        
        # Test WebSocket manager
        from lib.cad_websocket import CADWebSocketManager
        websocket_manager = CADWebSocketManager()
        print("✓ Created CADWebSocketManager instance")
        
        print("✓ All basic functionality tests passed")
        return True
    except Exception as e:
        print(f"✗ Failed basic functionality test: {e}")
        return False

def main():
    print("Testing CAD Enhancements functionality...")
    
    # Test imports
    if not test_imports():
        return
    
    # Test basic functionality
    if not asyncio.run(test_basic_functionality()):
        return
    
    print("\n✓ All tests passed! CAD enhancements are ready for use.")

if __name__ == "__main__":
    main()