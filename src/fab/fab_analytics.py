import asyncio
import json
import time
from datetime import datetime
from typing import Dict, Any
from src.lib.event_bus import event_bus
from src.lib.config_manager import config_manager
import logging

# Custom JSON Formatter for structured logging
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "service": "fab-service",
            "message": record.getMessage(),
            "latency": getattr(record, "latency", 0),
            "user_id": getattr(record, "user_id", "unknown"),
            "chip_id": getattr(record, "chip_id", "unknown"),
            "ai_operation_time": getattr(record, "ai_operation_time", 0)
        }
        return json.dumps(log_entry)

# Configure logging with JSON formatter
logger = logging.getLogger("fab-service")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)

class FabAnalytics:
    def __init__(self):
        self.metrics = {}

    async def collect_fab_metrics(self, fab_name: str) -> Dict[str, Any]:
        start_time = time.time()
        delay = config_manager.get("performance.simulation_delay", 0.1)
        await asyncio.sleep(delay)
        metrics = {
            "fab_name": fab_name,
            "production_rate": 80e15,
            "defect_rate": 0.0,
            "co2_emission": 0.0,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.metrics[fab_name] = metrics
        
        execution_time = time.time() - start_time
        # Log with structured logging
        logger.info(
            f"Fab metrics collected for {fab_name}",
            extra={
                "latency": execution_time,
                "user_id": "system",
                "chip_id": fab_name,  # Using fab_name as chip_id for identification
                "ai_operation_time": 0
            }
        )
        
        await event_bus.publish("ar_notification", {
            "message": f"Fab metrics collected for {fab_name} - HoloMisha programs the universe!",
            "lang": "uk"
        })
        
        await event_bus.publish("security_log", {
            "user_id": "system",
            "event_type": "fab_metrics_collection",
            "details": {"fab_name": fab_name}
        })
        return metrics

    async def analyze_fab_performance(self, fab_name: str, period: str = "24h") -> Dict[str, Any]:
        start_time = time.time()
        if fab_name not in self.metrics:
            execution_time = time.time() - start_time
            # Log with structured logging
            logger.warning(
                f"No metrics found for fab {fab_name}",
                extra={
                    "latency": execution_time,
                    "user_id": "system",
                    "chip_id": fab_name,  # Using fab_name as chip_id for identification
                    "ai_operation_time": 0
                }
            )
            
            await event_bus.publish("ar_notification", {
                "message": f"No metrics found for fab {fab_name} - HoloMisha programs the universe!",
                "lang": "uk"
            })
            
            await event_bus.publish("security_log", {
                "user_id": "system",
                "event_type": "fab_metrics_not_found",
                "details": {"fab_name": fab_name}
            })
            return {"status": "error", "message": "No metrics available"}
        
        execution_time = time.time() - start_time
        # Log with structured logging
        logger.info(
            f"Fab performance analyzed for {fab_name} over {period}",
            extra={
                "latency": execution_time,
                "user_id": "system",
                "chip_id": fab_name,  # Using fab_name as chip_id for identification
                "ai_operation_time": 0
            }
        )
        
        await event_bus.publish("ar_notification", {
            "message": f"Fab performance analyzed for {fab_name} over {period} - HoloMisha programs the universe!",
            "lang": "uk"
        })
        
        await event_bus.publish("security_log", {
            "user_id": "system",
            "event_type": "fab_performance_analysis",
            "details": {"fab_name": fab_name, "period": period}
        })
        return {"status": "success", "fab_name": fab_name, "metrics": self.metrics[fab_name]}