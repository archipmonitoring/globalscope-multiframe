import asyncio
import json
import time
from datetime import datetime
from typing import Dict, Any, List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.webxr.quest_master import QuestMaster

from src.webxr.holomisha_ar import holo_misha_instance
from src.webxr.quest_master import QuestMaster
from src.security.security_logging_service import SecurityLoggingService
from src.lib.utils import get_current_timestamp
import logging

# Custom JSON Formatter for structured logging
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "service": "community-service",
            "message": record.getMessage(),
            "latency": getattr(record, "latency", 0),
            "user_id": getattr(record, "user_id", "unknown"),
            "chip_id": getattr(record, "chip_id", "unknown"),
            "ai_operation_time": getattr(record, "ai_operation_time", 0)
        }
        return json.dumps(log_entry)

# Configure logging with JSON formatter
logger = logging.getLogger("community-service")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.webxr.quest_master import QuestMaster

quest_master: 'QuestMaster' = QuestMaster()
security_logger = SecurityLoggingService()

class CommunityEngine:
    def __init__(self):
        self.forums = {}
        self.global_chat = []

    async def create_forum(self, forum_id: str, title: str, user_id: str, lang: str = "uk") -> Dict[str, Any]:
        start_time = time.time()
        self.forums[forum_id] = {"title": title, "posts": [], "creator": user_id}
        await holo_misha_instance.notify_ar(f"Forum {title} created by {user_id} - HoloMisha programs the universe!", lang)
        await security_logger.log_security_event(user_id, "forum_creation", {"forum_id": forum_id, "title": title})
        
        execution_time = time.time() - start_time
        # Log with structured logging
        logger.info(
            f"Forum {title} created by {user_id}",
            extra={
                "latency": execution_time,
                "user_id": user_id,
                "chip_id": forum_id,  # Using forum_id as chip_id for identification
                "ai_operation_time": 0
            }
        )
        return {"status": "success", "forum_id": forum_id}

    async def add_post(self, forum_id: str, content: str, user_id: str, lang: str = "uk") -> Dict[str, Any]:
        start_time = time.time()
        if forum_id not in self.forums:
            await holo_misha_instance.notify_ar(f"Forum {forum_id} not found - HoloMisha programs the universe!", lang)
            await security_logger.log_security_event(user_id, "forum_not_found", {"forum_id": forum_id})
            
            execution_time = time.time() - start_time
            # Log with structured logging
            logger.warning(
                f"Forum {forum_id} not found",
                extra={
                    "latency": execution_time,
                    "user_id": user_id,
                    "chip_id": forum_id,  # Using forum_id as chip_id for identification
                    "ai_operation_time": 0
                }
            )
            return {"status": "error", "message": "Forum not found"}
        post_id = f"post_{len(self.forums[forum_id]['posts']) + 1}"
        self.forums[forum_id]["posts"].append({"post_id": post_id, "content": content, "user_id": user_id})
        await holo_misha_instance.notify_ar(f"Post added to forum {forum_id} by {user_id} - HoloMisha programs the universe!", lang)
        await security_logger.log_security_event(user_id, "post_addition", {"forum_id": forum_id, "post_id": post_id})
        
        execution_time = time.time() - start_time
        # Log with structured logging
        logger.info(
            f"Post added to forum {forum_id} by {user_id}",
            extra={
                "latency": execution_time,
                "user_id": user_id,
                "chip_id": forum_id,  # Using forum_id as chip_id for identification
                "ai_operation_time": 0
            }
        )
        return {"status": "success", "post_id": post_id}

    async def share_ip_block(self, ip_block_id: str, user_id: str, lang: str = "uk") -> Dict[str, Any]:
        start_time = time.time()
        # Використовуємо правильний метод з правильними параметрами
        update_method = getattr(quest_master, 'update_quest_progress', None)
        if update_method:
            await update_method(ip_block_id, [{"action": "share_ip_block", "ip_block_id": ip_block_id}])
        await holo_misha_instance.notify_ar(f"IP block {ip_block_id} shared by {user_id} - HoloMisha programs the universe!", lang)
        await security_logger.log_security_event(user_id, "ip_block_share", {"ip_block_id": ip_block_id})
        
        execution_time = time.time() - start_time
        # Log with structured logging
        logger.info(
            f"IP block {ip_block_id} shared by {user_id}",
            extra={
                "latency": execution_time,
                "user_id": user_id,
                "chip_id": ip_block_id,  # Using ip_block_id as chip_id for identification
                "ai_operation_time": 0
            }
        )
        return {"status": "success", "ip_block_id": ip_block_id}

    async def send_global_chat_message(self, user_id: str, message: str, lang: str = "uk") -> Dict[str, Any]:
        start_time = time.time()
        self.global_chat.append({"user_id": user_id, "message": message, "timestamp": get_current_timestamp()})
        await holo_misha_instance.notify_ar(f"Global chat message from {user_id}: {message} - HoloMisha programs the universe!", lang)
        await security_logger.log_security_event(user_id, "global_chat_message", {"message": message})
        
        execution_time = time.time() - start_time
        # Log with structured logging
        logger.info(
            f"Global chat message from {user_id}",
            extra={
                "latency": execution_time,
                "user_id": user_id,
                "chip_id": "global_chat",  # Using "global_chat" as chip_id for identification
                "ai_operation_time": 0
            }
        )
        return {"status": "success", "message_id": len(self.global_chat)}