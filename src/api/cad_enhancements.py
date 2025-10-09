"""
CAD Enhancements API for GlobalScope MultiFrame 11.0
This module provides REST API endpoints for CAD enhancements: caching, task queue, and WebSocket progress.
"""

from fastapi import APIRouter, HTTPException, Depends, WebSocket
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import logging
import asyncio

# Import our new modules
from src.lib.cad_cache import get_cad_cache, init_cad_cache
from src.lib.cad_queue import get_cad_queue, init_cad_queue, CADTask
from src.lib.cad_websocket import get_cad_websocket_manager, init_cad_websocket_manager

logger = logging.getLogger("CADEnhancementsAPI")
router = APIRouter(prefix="/api/v1/cad/enhancements", tags=["cad-enhancements"])

# Request models
class CacheInvalidateRequest(BaseModel):
    tool_name: Optional[str] = None
    project_id: Optional[str] = None

class TaskQueueRequest(BaseModel):
    tool_name: str
    params: Dict[str, Any]
    project_id: str
    priority: int = 0

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    tool_name: str
    project_id: str
    priority: int
    created_at: float
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class CacheStatsResponse(BaseModel):
    cache_enabled: bool
    default_ttl: int
    cache_prefix: str

# Initialize our modules when the API is imported
# In a real application, this would be done during app startup
_cad_cache = None
_cad_queue = None
_websocket_manager = None

async def initialize_modules():
    """Initialize our CAD enhancement modules"""
    global _cad_cache, _cad_queue, _websocket_manager
    if _cad_cache is None:
        _cad_cache = await init_cad_cache(None)  # Pass actual Redis client in real implementation
    if _cad_queue is None:
        _cad_queue = await init_cad_queue(5)  # 5 workers
    if _websocket_manager is None:
        _websocket_manager = init_cad_websocket_manager()

# Cache endpoints
@router.get("/cache/stats", response_model=CacheStatsResponse)
async def get_cache_stats():
    """Get cache statistics"""
    try:
        await initialize_modules()
        if _cad_cache is None:
            raise HTTPException(status_code=500, detail="Cache module not initialized")
        
        stats = await _cad_cache.get_cache_stats()
        return CacheStatsResponse(**stats)
    except Exception as e:
        logger.error(f"Error getting cache stats: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting cache stats: {str(e)}")

@router.post("/cache/invalidate")
async def invalidate_cache(request: CacheInvalidateRequest):
    """Invalidate cache entries"""
    try:
        await initialize_modules()
        if _cad_cache is None:
            raise HTTPException(status_code=500, detail="Cache module not initialized")
        
        await _cad_cache.invalidate_cache(request.tool_name, request.project_id)
        return {"status": "success", "message": "Cache invalidated"}
    except Exception as e:
        logger.error(f"Error invalidating cache: {e}")
        raise HTTPException(status_code=500, detail=f"Error invalidating cache: {str(e)}")

# Task queue endpoints
@router.post("/queue/task", response_model=Dict[str, str])
async def add_task_to_queue(request: TaskQueueRequest):
    """Add a task to the queue"""
    try:
        await initialize_modules()
        if _cad_queue is None:
            raise HTTPException(status_code=500, detail="Task queue module not initialized")
        
        task_id = await _cad_queue.add_task(
            tool_name=request.tool_name,
            params=request.params,
            project_id=request.project_id,
            priority=request.priority
        )
        
        return {"status": "success", "task_id": task_id}
    except Exception as e:
        logger.error(f"Error adding task to queue: {e}")
        raise HTTPException(status_code=500, detail=f"Error adding task to queue: {str(e)}")

@router.get("/queue/task/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """Get the status of a task"""
    try:
        await initialize_modules()
        if _cad_queue is None:
            raise HTTPException(status_code=500, detail="Task queue module not initialized")
        
        status = await _cad_queue.get_task_status(task_id)
        if status is None:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
        
        return TaskStatusResponse(**status)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting task status: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting task status: {str(e)}")

@router.get("/queue/tasks", response_model=List[TaskStatusResponse])
async def list_tasks(status: Optional[str] = None):
    """List all tasks, optionally filtered by status"""
    try:
        await initialize_modules()
        if _cad_queue is None:
            raise HTTPException(status_code=500, detail="Task queue module not initialized")
        
        tasks = await _cad_queue.list_tasks(status)
        return [TaskStatusResponse(**task) for task in tasks]
    except Exception as e:
        logger.error(f"Error listing tasks: {e}")
        raise HTTPException(status_code=500, detail=f"Error listing tasks: {str(e)}")

@router.delete("/queue/task/{task_id}", response_model=Dict[str, str])
async def cancel_task(task_id: str):
    """Cancel a pending task"""
    try:
        await initialize_modules()
        if _cad_queue is None:
            raise HTTPException(status_code=500, detail="Task queue module not initialized")
        
        result = await _cad_queue.cancel_task(task_id)
        if result:
            return {"status": "success", "message": f"Task {task_id} cancelled"}
        else:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found or not cancellable")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cancelling task: {e}")
        raise HTTPException(status_code=500, detail=f"Error cancelling task: {str(e)}")

# WebSocket endpoint
@router.websocket("/ws/progress/{task_id}")
async def websocket_progress_endpoint(websocket: WebSocket, task_id: str):
    """WebSocket endpoint for real-time task progress updates"""
    try:
        await initialize_modules()
        if _websocket_manager is None:
            raise HTTPException(status_code=500, detail="WebSocket manager not initialized")
        
        await _websocket_manager.connect(websocket, task_id)
        
        try:
            while True:
                # Keep the connection alive
                data = await websocket.receive_text()
                # Echo back for testing
                await websocket.send_text(f"Echo: {data}")
        except Exception as e:
            logger.info(f"WebSocket connection closed: {e}")
        finally:
            _websocket_manager.disconnect(websocket, task_id)
    except Exception as e:
        logger.error(f"Error in WebSocket connection: {e}")
        await websocket.close()

# Health check endpoint
@router.get("/health", response_model=Dict[str, str])
async def enhancements_health_check():
    """Check CAD enhancements system health"""
    try:
        await initialize_modules()
        
        # Check if modules are initialized
        cache_ok = _cad_cache is not None
        queue_ok = _cad_queue is not None
        websocket_ok = _websocket_manager is not None
        
        if cache_ok and queue_ok and websocket_ok:
            return {"status": "healthy", "message": "All CAD enhancements modules are running"}
        else:
            return {"status": "degraded", "message": "Some CAD enhancements modules are not initialized"}
    except Exception as e:
        logger.error(f"Error in enhancements health check: {e}")
        raise HTTPException(status_code=500, detail=f"Health check error: {str(e)}")