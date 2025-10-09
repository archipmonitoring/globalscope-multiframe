import asyncio
from typing import Dict, Any
from fastapi import WebSocket
import logging
from src.lib.event_bus import event_bus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("HoloMishaAR")

class HoloMishaAR:
    def __init__(self):
        self.websocket_uri = "/ws/ar"
        self.dashboard_state: Dict[str, Any] = {}
        self.active_connections = []
        
        # Subscribe to events
        event_bus.subscribe("ar_notification", self._handle_notification)
        event_bus.subscribe("dashboard_update", self._handle_dashboard_update)

    async def _broadcast(self, data: Dict[str, Any]):
        for connection in self.active_connections:
            try:
                await connection.send_json(data)
            except:
                self.active_connections.remove(connection)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        await self._broadcast({"status": "connected", "message": "HoloMisha programs the universe!"})

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        await self._broadcast({"status": "disconnected", "message": "HoloMisha programs the universe!"})
    
    async def notify_ar(self, message: str, lang: str = "uk"):
        """Send notification to AR interface"""
        await self._broadcast({"message": message, "lang": lang})
    
    async def update_ar_dashboard(self, data: Dict[str, Any]):
        """Update AR dashboard with new data"""
        self.dashboard_state.update(data)
        await self._broadcast({"dashboard_update": data})
    
    async def _handle_notification(self, event: Dict[str, Any]):
        """Handle AR notification events"""
        data = event["data"]
        await self.notify_ar(data["message"], data.get("lang", "uk"))
    
    async def _handle_dashboard_update(self, event: Dict[str, Any]):
        """Handle dashboard update events"""
        data = event["data"]
        await self.update_ar_dashboard(data)

# Global instance
holo_misha_instance = HoloMishaAR()