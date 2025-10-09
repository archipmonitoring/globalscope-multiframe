import asyncio
from typing import Dict, Any
from src.webxr.holomisha_ar import holo_misha_instance
from src.security.security_logging_service import SecurityLoggingService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AgentGuard")
security_logger = SecurityLoggingService()

class AgentState:
    ACTIVE = "active"
    SLEEPING = "sleeping"
    ERROR = "error"
    MAINTENANCE = "maintenance"

class AgentGuard:
    def __init__(self):
        self.agent_states: Dict[str, str] = {}
        self.agent_health: Dict[str, Dict[str, Any]] = {}

    async def monitor_agents(self, agent_states_dict: Dict[str, str]):
        self.agent_states.update(agent_states_dict)
        for agent_id, state in agent_states_dict.items():
            if state == AgentState.ERROR:
                await self.put_agent_to_sleep(agent_id, "Error detected")
        await holo_misha_instance.notify_ar(f"Agents monitored: {len(agent_states_dict)} - HoloMisha programs the universe!", "uk")
        await security_logger.log_security_event("system", "agent_monitoring", {"agent_count": len(agent_states_dict)})

    async def put_agent_to_sleep(self, agent_id: str, reason: str = "Unknown reason"):
        self.agent_states[agent_id] = AgentState.SLEEPING
        logger.info(f"Agent {agent_id} put to sleep: {reason}")
        await holo_misha_instance.notify_ar(f"Agent {agent_id} put to sleep: {reason} - HoloMisha programs the universe!", "uk")
        await security_logger.log_security_event("system", "agent_sleep", {"agent_id": agent_id, "reason": reason})