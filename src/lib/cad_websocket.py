import asyncio
import json
from typing import Dict, Any, Optional, Set
from dataclasses import dataclass, asdict
import time
from datetime import datetime

# Assuming we have a connection manager from FastAPI/Starlette
from fastapi import WebSocket, WebSocketDisconnect

@dataclass
class SimulationProgress:
    """Represents the progress of a CAD simulation"""
    task_id: str
    tool_name: str
    project_id: str
    stage: str  # e.g., "parsing", "elaboration", "optimization", "generation"
    progress: float  # 0.0 to 1.0
    message: str
    timestamp: Optional[float] = None
    metrics: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


class CADWebSocketManager:
    """Manages WebSocket connections for real-time simulation progress updates"""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.task_subscriptions: Dict[str, Set[WebSocket]] = {}  # task_id -> set of connections
        self.task_progress: Dict[str, SimulationProgress] = {}  # task_id -> latest progress
        
    async def connect(self, websocket: WebSocket, task_id: str):
        """Accept WebSocket connection and subscribe to task updates"""
        await websocket.accept()
        self.active_connections.add(websocket)
        
        # Subscribe to specific task
        if task_id not in self.task_subscriptions:
            self.task_subscriptions[task_id] = set()
        self.task_subscriptions[task_id].add(websocket)
        
        # Send current progress if available
        if task_id in self.task_progress:
            progress = self.task_progress[task_id]
            await self._send_progress_update(websocket, progress)
        
        # Send connection established message
        await self._send_progress_update(websocket, SimulationProgress(
            task_id=task_id,
            tool_name="system",
            project_id="unknown",
            stage="connected",
            progress=0.0,
            message="Connected to simulation progress stream"
        ))
        
    def disconnect(self, websocket: WebSocket, task_id: str):
        """Remove WebSocket connection and unsubscribe from task"""
        self.active_connections.discard(websocket)
        
        # Unsubscribe from task
        if task_id in self.task_subscriptions:
            self.task_subscriptions[task_id].discard(websocket)
            # Clean up empty subscriptions
            if len(self.task_subscriptions[task_id]) == 0:
                del self.task_subscriptions[task_id]
        
    async def update_progress(self, task_id: str, stage: str, progress: float, message: str, tool_name: str = "unknown", project_id: str = "unknown", metrics: Optional[Dict[str, Any]] = None):
        """Update progress for a task and broadcast to all subscribed clients"""
        # Create progress update
        progress_update = SimulationProgress(
            task_id=task_id,
            tool_name=tool_name,
            project_id=project_id,
            stage=stage,
            progress=progress,
            message=message,
            metrics=metrics
        )
        
        # Store latest progress
        self.task_progress[task_id] = progress_update
        
        # Broadcast to all subscribers
        if task_id in self.task_subscriptions:
            disconnected = []
            for connection in self.task_subscriptions[task_id]:
                try:
                    await self._send_progress_update(connection, progress_update)
                except RuntimeError:
                    # Connection is closed
                    disconnected.append(connection)
                
            # Clean up disconnected clients
            for conn in disconnected:
                self.disconnect(conn, task_id)
        
    async def _send_progress_update(self, websocket: WebSocket, progress: SimulationProgress):
        """Send progress update to a single client"""
        try:
            await websocket.send_text(json.dumps({
                "type": "progress_update",
                "data": asdict(progress)
            }))
        except RuntimeError:
            # Client disconnected
            pass
        
    async def get_current_progress(self, task_id: str) -> Optional[SimulationProgress]:
        """Get the current progress for a task"""
        return self.task_progress.get(task_id)
        
    async def broadcast_system_message(self, message: str, severity: str = "info"):
        """Broadcast a system message to all connected clients"""
        # Create a special system message
        system_msg = {
            "type": "system_message",
            "data": {
                "message": message,
                "severity": severity,
                "timestamp": time.time()
            }
        }
        
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(system_msg))
            except RuntimeError:
                disconnected.append(connection)
                
        # Clean up disconnected clients
        for conn in disconnected:
            self.active_connections.discard(conn)

# Global instance will be created when imported
_websocket_manager = None
def get_cad_websocket_manager():
    """Get the global CADWebSocketManager instance
    
    Returns:
        CADWebSocketManager: The global WebSocket manager instance
    """
    global _websocket_manager
    return _websocket_manager

def init_cad_websocket_manager():
    """Initialize the global CADWebSocketManager instance
    
    Returns:
        CADWebSocketManager: Initialized WebSocket manager instance
    """
    global _websocket_manager
    _websocket_manager = CADWebSocketManager()
    return _websocket_manager