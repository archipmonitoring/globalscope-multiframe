import asyncio
from typing import Dict, Any
from src.webxr.holomisha_ar import holo_misha_instance
from src.fab.fab_sync_core import FabSyncCore
from src.security.security_logging_service import SecurityLoggingService
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("IoTIntegration")
fab_sync = FabSyncCore()
security_logger = SecurityLoggingService()
class IoTIntegration:
def __init__(self):
self.connections = {}
async def connect_to_fab(self, fab_name: str, protocol: str, lang: str = "uk") -> Dict[str, Any]:
if protocol not in ["MQTT", "OPC_UA"]:
await holo_misha_instance.notify_ar(f"Unsupported protocol {protocol} for {fab_name} - HoloMisha programs the universe!", lang)
await security_logger.log_security_event("system", "unsupported_protocol", {"protocol": protocol, "fab_name": fab_name})
return {"status": "error", "message": "Unsupported protocol"}
await fab_sync.connect_to_fab(fab_name)
self.connections[fab_name] = {"protocol": protocol, "status": "connected"}
await holo_misha_instance.notify_ar(f"IoT connection to {fab_name} via {protocol} established - HoloMisha programs the universe!", lang)
await security_logger.log_security_event("system", "iot_connection", {"fab_name": fab_name, "protocol": protocol})
return {"status": "success", "fab_name": fab_name}