import asyncio
import json
from redis.asyncio import Redis
from typing import Dict, Any
from datetime import datetime
from src.lib.utils import get_logger
from src.lib.event_bus import event_bus

redis_client = Redis(host="redis-master", port=6379)
logger = get_logger("SecurityLoggingService")

class SecurityLoggingService:
    def __init__(self):
        self.logs = {}
        # Subscribe to security events
        event_bus.subscribe("security_log", self._handle_security_event)

    async def log_security_event(self, user_id: str, event_type: str, details: Dict[str, Any]):
        event_id = f"event_{user_id}_{await redis_client.incr('event_counter')}"
        log_data = {
            "event_id": event_id,
            "user_id": user_id,
            "event_type": event_type,
            "details": details,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.logs[event_id] = log_data
        await redis_client.set(f"security_log:{event_id}", json.dumps(log_data))
        
        # Notify through event bus instead of direct import
        await event_bus.publish("ar_notification", {
            "message": f"Security event {event_type} logged for {user_id} - HoloMisha programs the universe!",
            "lang": "uk"
        })
    
    async def _handle_security_event(self, event: Dict[str, Any]):
        """Handle security log events from the event bus"""
        data = event["data"]
        await self.log_security_event(data["user_id"], data["event_type"], data["details"])

# Global instance
security_logger = SecurityLoggingService()