import asyncio
from typing import Dict, Any
from datetime import datetime, timedelta
from src.lib.event_bus import event_bus
from src.lib.config_manager import config_manager
from src.lib.redis_client import redis_client
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ChipAnalytics")

class ChipAnalytics:
    def __init__(self):
        self.metrics_history: Dict[str, Any] = {}

    async def collect_metrics(self, chip_id: str) -> Dict[str, Any]:
        delay = config_manager.get("performance.simulation_delay", 0.1)
        await asyncio.sleep(delay)
        metrics = {
            "chip_id": chip_id,
            "defect_rate": 0.0,
            "yield": 0.9999999999999999,
            "energy_consumption": 0.008,
            "co2_emission": 0.0,
            "temperature": 25.0,
            "voltage": 1.2,
            "frequency": 3.5,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if chip_id not in self.metrics_history:
            self.metrics_history[chip_id] = []
        self.metrics_history[chip_id].append(metrics)
        self.metrics_history[chip_id] = self.metrics_history[chip_id][-100:]  # Keep last 100 entries
        
        # Store metrics in Redis with caching
        await redis_client.set_json(f"analytics:metrics:{chip_id}", metrics, ex=3600, use_cache=True)  # 1 hour expiration
        
        # Use event bus instead of direct imports
        await event_bus.publish("ar_notification", {
            "message": f"Metrics collected for chip {chip_id} - HoloMisha programs the universe!",
            "lang": "uk"
        })
        
        await event_bus.publish("security_log", {
            "user_id": "system",
            "event_type": "metrics_collection",
            "details": {"chip_id": chip_id}
        })
        return metrics

    async def get_metrics(self, chip_id: str) -> Dict[str, Any]:
        # Try to get from cache first
        cached_metrics = await redis_client.get_json(f"analytics:metrics:{chip_id}", use_cache=True)
        if cached_metrics:
            await event_bus.publish("ar_notification", {
                "message": f"Latest metrics retrieved for chip {chip_id} - HoloMisha programs the universe!",
                "lang": "uk"
            })
            
            await event_bus.publish("security_log", {
                "user_id": "system",
                "event_type": "metrics_retrieval",
                "details": {"chip_id": chip_id}
            })
            return cached_metrics
        
        if chip_id not in self.metrics_history or not self.metrics_history[chip_id]:
            await event_bus.publish("ar_notification", {
                "message": f"No metrics found for chip {chip_id} - HoloMisha programs the universe!",
                "lang": "uk"
            })
            
            await event_bus.publish("security_log", {
                "user_id": "system",
                "event_type": "metrics_not_found",
                "details": {"chip_id": chip_id}
            })
            return {"status": "error", "message": "No metrics available"}
        
        metrics = self.metrics_history[chip_id][-1]
        # Cache the result
        await redis_client.set_json(f"analytics:metrics:{chip_id}", metrics, ex=3600, use_cache=True)
        
        await event_bus.publish("ar_notification", {
            "message": f"Latest metrics retrieved for chip {chip_id} - HoloMisha programs the universe!",
            "lang": "uk"
        })
        
        await event_bus.publish("security_log", {
            "user_id": "system",
            "event_type": "metrics_retrieval",
            "details": {"chip_id": chip_id}
        })
        return metrics

    async def analyze_trends(self, chip_id: str, hours: int = 24) -> Dict[str, Any]:
        # Try to get from cache first
        cache_key = f"analytics:trends:{chip_id}:{hours}"
        cached_trends = await redis_client.get_json(cache_key, use_cache=True)
        if cached_trends:
            await event_bus.publish("ar_notification", {
                "message": f"Trends analyzed for chip {chip_id} over {hours} hours - HoloMisha programs the universe!",
                "lang": "uk"
            })
            
            await event_bus.publish("security_log", {
                "user_id": "system",
                "event_type": "trend_analysis",
                "details": {"chip_id": chip_id, "hours": hours}
            })
            return cached_trends
        
        if chip_id not in self.metrics_history:
            await event_bus.publish("ar_notification", {
                "message": f"No trend data for chip {chip_id} - HoloMisha programs the universe!",
                "lang": "uk"
            })
            
            await event_bus.publish("security_log", {
                "user_id": "system",
                "event_type": "trend_data_not_found",
                "details": {"chip_id": chip_id}
            })
            return {"status": "error", "message": "No data available"}
        
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        filtered_metrics = [m for m in self.metrics_history[chip_id] if datetime.fromisoformat(m["timestamp"]) > cutoff_time]
        
        result = {"status": "success", "chip_id": chip_id, "trends": filtered_metrics}
        
        # Cache the result for 30 minutes
        await redis_client.set_json(cache_key, result, ex=1800, use_cache=True)
        
        await event_bus.publish("ar_notification", {
            "message": f"Trends analyzed for chip {chip_id} over {hours} hours - HoloMisha programs the universe!",
            "lang": "uk"
        })
        
        await event_bus.publish("security_log", {
            "user_id": "system",
            "event_type": "trend_analysis",
            "details": {"chip_id": chip_id, "hours": hours}
        })
        return result