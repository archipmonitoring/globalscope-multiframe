import asyncio
import sys
from src.lib.cad_queue import CADTaskQueue, init_cad_queue, get_cad_queue

def print_available_modules():
    """Print available modules to debug import issues"""
    print("Python path:")
    for path in sys.path:
        print(f"  {path}")
    
    print("\nAvailable modules:")
    # Try to import our module directly
    try:
        from src.lib.cad_queue import CADTaskQueue, init_cad_queue
        print("✓ Successfully imported cad_queue")
        return True
    except Exception as e:
        print(f"✗ Failed to import cad_queue: {e}")
        return False

def main():
    print("Testing CAD Task Queue functionality...")
    
    # First check if we can import the module
    if not print_available_modules():
        return
    
    # Test basic functionality
    try:
        # Create queue
        queue = CADTaskQueue(max_workers=2)
        print("✓ Created CADTaskQueue instance")
        
        # Initialize it
        asyncio.run(init_cad_queue(2))
        print("✓ Initialized CADTaskQueue")
        
        # Add a task
        async def add_and_check_task():
            task_id = await queue.add_task(
                tool_name="verilator",
                params={"input": "test.v"},
                project_id="proj_123"
            )
            print(f"✓ Added task with ID: {task_id}")
            
            # Get task status
            status = await queue.get_task_status(task_id)
            if status:
                print(f"✓ Got task status: {status['status']}")
            else:
                print("✗ Failed to get task status")
            
            # List tasks
            tasks = await queue.list_tasks()
            print(f"✓ Listed {len(tasks)} tasks")
            
            # Cancel task (if still pending)
            cancelled = await queue.cancel_task(task_id)
            print(f"✓ Cancelled task: {cancelled}")
            
            # Stop queue
            await queue.stop()
            print("✓ Stopped queue")
        
        asyncio.run(add_and_check_task())
        
    except Exception as e:
        print(f"✗ Error during test: {e}")

if __name__ == "__main__":
    main()