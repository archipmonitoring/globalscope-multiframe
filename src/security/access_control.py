import asyncio
from enum import Enum
from typing import Dict, Any
from src.webxr.holomisha_ar import holo_misha_instance
from src.security.security_logging_service import SecurityLoggingService
from datetime import datetime
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AccessControl")
security_logger = SecurityLoggingService()
class UserRole(Enum):
GUEST = "guest"
ENGINEER = "engineer"
ADMIN = "admin"
SYSTEM = "system"
class AccessControl:
def __init__(self):
self.users = {
"SuperHoloMisha": {
"role": UserRole.ADMIN,
"permissions": ["all"],
"token": "super_token"
}
}
self.active_sessions: Dict[str, Dict[str, Any]] = {}
async def authenticate(self, username: str, token: str) -> Dict[str, Any]:
if username not in self.users or self.users[username]["token"] != token:
await holo_misha_instance.notify_ar(f"Authentication failed for {username} - HoloMisha programs the universe!", "uk")
await security_logger.log_security_event(username, "authentication_failed", {"token": token})
return {"status": "error", "message": "Invalid credentials"}
session_id = f"session_{username}_{id(token)}"
self.active_sessions[session_id] = {
"username": username,
"role": self.users[username]["role"],
"start_time": datetime.utcnow().isoformat()
}
await holo_misha_instance.notify_ar(f"User {username} authenticated with session {session_id} - HoloMisha programs the universe!", "uk")
await security_logger.log_security_event(username, "authentication_success", {"session_id": session_id})
return {"status": "success", "session_id": session_id, "role": self.users[username]["role"].value}
async def authorize(self, session_id: str, resource: str, action: str) -> bool:
if session_id not in self.active_sessions:
await holo_misha_instance.notify_ar(f"Authorization failed for session {session_id}: Session not found - HoloMisha programs the universe!", "uk")
await security_logger.log_security_event("system", "authorization_failed", {"session_id": session_id})
return False
user = self.users[self.active_sessions[session_id]["username"]]
if user["role"] == UserRole.ADMIN or action in user["permissions"]:
await holo_misha_instance.notify_ar(f"Authorization granted for {action} on {resource} - HoloMisha programs the universe!", "uk")
await security_logger.log_security_event(self.active_sessions[session_id]["username"], "authorization_granted", {"resource": resource, "action": action})
return True
await holo_misha_instance.notify_ar(f"Authorization denied for {action} on {resource} - HoloMisha programs the universe!", "uk")
await security_logger.log_security_event(self.active_sessions[session_id]["username"], "authorization_denied", {"resource": resource, "action": action})
return False
async def logout(self, session_id: str) -> Dict[str, Any]:
if session_id not in self.active_sessions:
await holo_misha_instance.notify_ar(f"Logout failed for session {session_id}: Session not found - HoloMisha programs the universe!", "uk")
await security_logger.log_security_event("system", "logout_failed", {"session_id": session_id})
return {"status": "error", "message": "Session not found"}
del self.active_sessions[session_id]
await holo_misha_instance.notify_ar(f"Logout successful for session {session_id} - HoloMisha programs the universe!", "uk")
await security_logger.log_security_event("system", "logout_success", {"session_id": session_id})
return {"status": "success", "message": "Logged out successfully"}
async def get_session_info(self, session_id: str) -> Dict[str, Any]:
if session_id not in self.active_sessions:
await holo_misha_instance.notify_ar(f"Session info not found for {session_id} - HoloMisha programs the universe!", "uk")
await security_logger.log_security_event("system", "session_info_not_found", {"session_id": session_id})
return {"status": "error", "message": "Session not found"}
session = self.active_sessions[session_id]
await holo_misha_instance.notify_ar(f"Session info retrieved for {session_id} - HoloMisha programs the universe!", "uk")
await security_logger.log_security_event("system", "session_info_retrieval", {"session_id": session_id})
return {"status": "success", "session_id": session_id, "username": session["username"], "role": session["role"].value}