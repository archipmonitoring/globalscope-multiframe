import asyncio
import json
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass, asdict
import time

@dataclass
class CADTask:
    """Represents a CAD tool execution task"""
    task_id: str
    tool_name: str
    params: Dict[str, Any]
    project_id: str
    priority: int = 0
    created_at: float = None
    status: str = "pending"  # pending, running, completed, failed
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()


class CADTaskQueue:
    """Task queue system for handling parallel CAD operations"""
    
    def __init__(self, max_workers: int = 5):
        self.max_workers = max_workers
        self.tasks: Dict[str, CADTask] = {}
        self.task_queue = asyncio.PriorityQueue()
        self.workers = []
        self.running = False
        
    async def start(self):
        """Start the task queue and workers"""
        if self.running:
            return
            
        self.running = True
        # Start worker tasks
        self.workers = [
            asyncio.create_task(self._worker(i)) 
            for i in range(self.max_workers)
        ]
        
    async def stop(self):
        """Stop the task queue and workers"""
        self.running = False
        # Put sentinel values to wake up workers
        for _ in range(self.max_workers):
            await self.task_queue.put((float('inf'), None))
        # Wait for workers to finish
        if self.workers:
            await asyncio.gather(*self.workers, return_exceptions=True)
        
    async def add_task(self, tool_name: str, params: Dict[str, Any], project_id: str, priority: int = 0) -> str:
        """Add a new task to the queue
        
        Args:
            tool_name: Name of the CAD tool to run
            params: Parameters for the CAD tool
            project_id: ID of the project
            priority: Task priority (lower number = higher priority)
            
        Returns:
            str: Task ID
        """
        task_id = f"{tool_name}_{int(time.time()*1000)}_{project_id[-4:] if project_id else ''}"
        task = CADTask(
            task_id=task_id,
            tool_name=tool_name,
            params=params,
            project_id=project_id,
            priority=priority
        )
        self.tasks[task_id] = task
        
        # Priority queue uses lowest value first, so negate priority for proper ordering
        await self.task_queue.put((-priority, task_id))
        
        return task_id
    
    async def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a task"""
        if task_id not in self.tasks:
            return None
            
        task = self.tasks[task_id]
        return {
            'task_id': task.task_id,
            'status': task.status,
            'tool_name': task.tool_name,
            'project_id': task.project_id,
            'priority': task.priority,
            'created_at': task.created_at,
            'result': task.result,
            'error': task.error
        }
    
    async def _worker(self, worker_id: int):
        """Worker coroutine that processes tasks"""
        while self.running:
            try:
                # Get task from queue (this will block until a task is available)
                priority, task_id = await self.task_queue.get()
                
                # Check for sentinel value to stop
                if task_id is None:
                    break
                    
                if task_id not in self.tasks:
                    continue
                    
                task = self.tasks[task_id]
                task.status = "running"
                
                try:
                    # Here we would call the actual CAD tool
                    # For now, simulate work with sleep
                    print(f"Worker {worker_id} starting task {task_id} ({task.tool_name})")
                    
                    # Simulate CAD tool execution
                    # In real implementation, this would call the actual CAD tool
                    await asyncio.sleep(2)  # Simulate work
                    
                    # Simulate result
                    task.result = {
                        "success": True,
                        "output": f"Simulated output from {task.tool_name}",
                        "metrics": {
                            "execution_time": 2.0,
                            "memory_usage": 100.0
                        }
                    }
                    task.status = "completed"
                    
                    print(f"Worker {worker_id} completed task {task_id}")
                    
                except Exception as e:
                    task.status = "failed"
                    task.error = str(e)
                    print(f"Worker {worker_id} failed task {task_id}: {e}")
                    
                finally:
                    # Mark task as done in queue
                    self.task_queue.task_done()
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Worker {worker_id} encountered error: {e}")
                # Prevent tight loop on error
                await asyncio.sleep(1)
    
    async def list_tasks(self, status: Optional[str] = None) -> list:
        """List all tasks, optionally filtered by status"""
        tasks = []
        for task in self.tasks.values():
            if status is None or task.status == status:
                tasks.append({
                    'task_id': task.task_id,
                    'status': task.status,
                    'tool_name': task.tool_name,
                    'project_id': task.project_id,
                    'priority': task.priority,
                    'created_at': task.created_at
                })
        # Sort by creation time (newest first)
        tasks.sort(key=lambda x: x['created_at'], reverse=True)
        return tasks
    
    async def cancel_task(self, task_id: str) -> bool:
        """Cancel a pending task"""
        if task_id not in self.tasks:
            return False
            
        task = self.tasks[task_id]
        if task.status != "pending":
            return False  # Can only cancel pending tasks
            
        # Remove from our tasks dict
        del self.tasks[task_id]
        # Note: We can't easily remove from PriorityQueue, but the worker will skip it
        task.status = "cancelled"
        return True

# Global instance will be created when imported
_cad_queue = None
def get_cad_queue():
    """Get the global CADTaskQueue instance
    
    Returns:
        CADTaskQueue: The global task queue instance
    """
    global _cad_queue
    return _cad_queue

async def init_cad_queue(max_workers: int = 5):
    """Initialize the global CADTaskQueue instance
    
    Args:
        max_workers: Number of worker threads to use
        
    Returns:
        CADTaskQueue: Initialized task queue instance
    """
    global _cad_queue
    _cad_queue = CADTaskQueue(max_workers)
    await _cad_queue.start()
    return _cad_queue