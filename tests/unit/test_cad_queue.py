import asyncio
import pytest
from unittest.mock import Mock, AsyncMock

# Import our modules
from src.lib.cad_queue import CADTaskQueue, CADTask, init_cad_queue, get_cad_queue

def test_cad_task_creation():
    """Test basic CADTask creation and properties"""
    task = CADTask(
        task_id="test_123",
        tool_name="verilator",
        params={"input": "test.v"},
        project_id="proj_456"
    )
    
    assert task.task_id == "test_123"
    assert task.tool_name == "verilator"
    assert task.params == {"input": "test.v"}
    assert task.project_id == "proj_456"
    assert task.status == "pending"
    assert task.created_at is not None
    
    # Test priority default
    assert task.priority == 0
    
    # Test custom priority
    task_high = CADTask(
        task_id="test_123",
        tool_name="verilator",
        params={"input": "test.v"},
        project_id="proj_456",
        priority=10
    )
    assert task_high.priority == 10

class TestCADTaskQueue:
    @pytest.fixture(autouse=True)
    async def setup_teardown(self):
        """Setup and teardown for each test"""
        # Reset global instance
        from src.lib.cad_queue import _cad_queue
        global _cad_queue
        _cad_queue = None
        
        yield
        
        # Cleanup
        if get_cad_queue() is not None:
            await get_cad_queue().stop()
    
    async def test_queue_initialization(self):
        """Test CADTaskQueue initialization"""
        queue = CADTaskQueue(max_workers=3)
        
        assert queue.max_workers == 3
        assert len(queue.tasks) == 0
        assert queue.running == False
        
    async def test_init_and_get_queue(self):
        """Test initialization and retrieval of global queue instance"""
        # Initialize queue
        queue = await init_cad_queue(max_workers=2)
        
        assert queue is not None
        assert isinstance(queue, CADTaskQueue)
        assert queue.max_workers == 2
        assert queue.running == True
        
        # Get same instance
        queue2 = get_cad_queue()
        assert queue2 is queue
        
    async def test_add_task(self):
        """Test adding a task to the queue"""
        queue = await init_cad_queue(max_workers=1)
        
        # Add a task
        task_id = await queue.add_task(
            tool_name="verilator",
            params={"input": "test.v"},
            project_id="proj_123",
            priority=5
        )
        
        assert task_id is not None
        assert task_id in queue.tasks
        
        task = queue.tasks[task_id]
        assert task.tool_name == "verilator"
        assert task.params == {"input": "test.v"}
        assert task.project_id == "proj_123"
        assert task.priority == 5
        assert task.status == "pending"
        
    async def test_task_execution(self):
        """Test that tasks are executed by workers"""
        queue = await init_cad_queue(max_workers=1)
        
        # Add a task
        task_id = await queue.add_task(
            tool_name="verilator",
            params={"input": "test.v"},
            project_id="proj_123"
        )
        
        # Wait a moment for worker to process
        await asyncio.sleep(0.1)
        
        # Check task status
        status = await queue.get_task_status(task_id)
        assert status is not None
        assert status["status"] == "completed"
        assert status["result"] is not None
        assert status["error"] is None
        
    async def test_multiple_tasks(self):
        """Test handling multiple tasks with different priorities"""
        queue = await init_cad_queue(max_workers=2)
        
        # Add multiple tasks with different priorities
        task_ids = []
        for i in range(5):
            priority = i % 3  # Vary priorities
            task_id = await queue.add_task(
                tool_name=f"tool_{i}",
                params={"input": f"test_{i}.v"},
                project_id="proj_123",
                priority=priority
            )
            task_ids.append(task_id)
        
        # Wait for processing
        await asyncio.sleep(0.5)
        
        # Check all tasks were processed
        for task_id in task_ids:
            status = await queue.get_task_status(task_id)
            assert status is not None
            assert status["status"] in ["completed", "running"]  # Could still be running
        
    async def test_list_tasks(self):
        """Test listing tasks"""
        queue = await init_cad_queue(max_workers=1)
        
        # Add some tasks
        task_ids = []
        for i in range(3):
            task_id = await queue.add_task(
                tool_name=f"tool_{i}",
                params={"input": f"test_{i}.v"},
                project_id="proj_123"
            )
            task_ids.append(task_id)
        
        # Wait a bit
        await asyncio.sleep(0.1)
        
        # List all tasks
        tasks = await queue.list_tasks()
        assert len(tasks) >= 3  # At least 3 tasks
        
        # List pending tasks
        pending = await queue.list_tasks(status="pending")
        completed = await queue.list_tasks(status="completed")
        
        # Some should be completed, none should be pending (if fast enough)
        assert len(completed) > 0
        
    async def test_cancel_task(self):
        """Test task cancellation"""
        queue = await init_cad_queue(max_workers=1)
        
        # Add a task
        task_id = await queue.add_task(
            tool_name="verilator",
            params={"input": "test.v"},
            project_id="proj_123"
        )
        
        # Cancel before execution
        result = await queue.cancel_task(task_id)
        assert result == True
        
        # Task should no longer be in tasks
        assert task_id not in queue.tasks
        
        # Cannot cancel non-existent task
        result = await queue.cancel_task("nonexistent")
        assert result == False
        
        # Cannot cancel running task (though hard to test directly)
        # This would require more complex mocking
    
    async def test_get_task_status(self):
        """Test getting task status"""
        queue = await init_cad_queue(max_workers=1)
        
        # Add a task
        task_id = await queue.add_task(
            tool_name="verilator",
            params={"input": "test.v"},
            project_id="proj_123"
        )
        
        # Get status
        status = await queue.get_task_status(task_id)
        assert status is not None
        assert status["task_id"] == task_id
        assert status["tool_name"] == "verilator"
        assert status["project_id"] == "proj_123"
        assert status["status"] in ["pending", "running", "completed"]
        
        # Non-existent task
        status = await queue.get_task_status("nonexistent")
        assert status is None