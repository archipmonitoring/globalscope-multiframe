"""
Unit tests for CAD WebSocket functionality
"""
import pytest
import asyncio
import json
from unittest.mock import Mock, AsyncMock

# Import our modules
from src.lib.cad_websocket import CADWebSocketManager, init_cad_websocket_manager, get_cad_websocket_manager

class MockWebSocket:
    """Mock WebSocket for testing"""
    def __init__(self):
        self.sent_messages = []
        self.accepted = False
        self.closed = False
    
    async def accept(self):
        self.accepted = True
    
    async def send_text(self, message):
        self.sent_messages.append(message)
    
    async def close(self):
        self.closed = True

class TestCADWebSocketManager:
    @pytest.fixture
    def websocket_manager(self):
        """Create a CADWebSocketManager instance"""
        return CADWebSocketManager()
    
    def test_init(self):
        """Test CADWebSocketManager initialization"""
        manager = CADWebSocketManager()
        assert len(manager.active_connections) == 0
        assert len(manager.task_subscriptions) == 0
        assert len(manager.task_progress) == 0
    
    async def test_connect_and_disconnect(self, websocket_manager):
        """Test connecting and disconnecting WebSocket"""
        websocket = MockWebSocket()
        task_id = "test_task_123"
        
        # Connect
        await websocket_manager.connect(websocket, task_id)
        
        # Verify connection
        assert websocket.accepted == True
        assert websocket in websocket_manager.active_connections
        assert websocket in websocket_manager.task_subscriptions[task_id]
        
        # Disconnect
        websocket_manager.disconnect(websocket, task_id)
        
        # Verify disconnection
        assert websocket not in websocket_manager.active_connections
        assert task_id not in websocket_manager.task_subscriptions
    
    async def test_update_progress(self, websocket_manager):
        """Test updating progress and broadcasting to subscribers"""
        websocket = MockWebSocket()
        task_id = "test_task_123"
        
        # Connect websocket to task
        await websocket_manager.connect(websocket, task_id)
        
        # Update progress
        await websocket_manager.update_progress(
            task_id=task_id,
            stage="parsing",
            progress=0.5,
            message="Parsing Verilog files",
            tool_name="verilator",
            project_id="proj_456"
        )
        
        # Verify message was sent
        assert len(websocket.sent_messages) == 2  # Connection message + progress update
        message = json.loads(websocket.sent_messages[1])
        assert message["type"] == "progress_update"
        assert message["data"]["task_id"] == task_id
        assert message["data"]["stage"] == "parsing"
        assert message["data"]["progress"] == 0.5
    
    async def test_get_current_progress(self, websocket_manager):
        """Test getting current progress for a task"""
        task_id = "test_task_123"
        
        # Update progress
        await websocket_manager.update_progress(
            task_id=task_id,
            stage="synthesis",
            progress=0.75,
            message="Synthesizing design",
            tool_name="yosys",
            project_id="proj_456"
        )
        
        # Get progress
        progress = await websocket_manager.get_current_progress(task_id)
        
        # Verify
        assert progress is not None
        assert progress.task_id == task_id
        assert progress.stage == "synthesis"
        assert progress.progress == 0.75
        assert progress.message == "Synthesizing design"
    
    async def test_broadcast_system_message(self, websocket_manager):
        """Test broadcasting system messages"""
        websocket = MockWebSocket()
        task_id = "test_task_123"
        
        # Connect websocket
        await websocket_manager.connect(websocket, task_id)
        
        # Broadcast system message
        await websocket_manager.broadcast_system_message("System maintenance starting", "warning")
        
        # Verify message was sent
        assert len(websocket.sent_messages) == 2  # Connection message + system message
        message = json.loads(websocket.sent_messages[1])
        assert message["type"] == "system_message"
        assert message["data"]["message"] == "System maintenance starting"
        assert message["data"]["severity"] == "warning"
    
    async def test_init_and_get_cad_websocket_manager(self):
        """Test initializing and getting the global WebSocket manager instance"""
        # Initialize
        manager = init_cad_websocket_manager()
        
        # Verify initialization
        assert isinstance(manager, CADWebSocketManager)
        
        # Verify global instance
        global_manager = get_cad_websocket_manager()
        assert global_manager is manager

if __name__ == "__main__":
    pytest.main([__file__])