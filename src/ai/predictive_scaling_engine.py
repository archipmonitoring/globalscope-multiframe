from dataclasses import dataclass
from typing import List, Dict, Any
import asyncio
import logging
from src.webxr.holomisha_ar import holo_misha_instance
from src.security.security_logging_service import SecurityLoggingService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PredictiveScalingEngine")
security_logger = SecurityLoggingService()

@dataclass
class ScalingRecommendation:
    predicted_load: float
    current_resources: int
    recommended_resources: int
    reason: str

class PredictiveScalingModel:
    async def predict(self, metrics_history: List[Dict[str, Any]]) -> float:
        raise NotImplementedError

class ExponentialSmoothingModel(PredictiveScalingModel):
    def __init__(self, alpha: float = 0.3):
        self.alpha = alpha

    async def predict(self, metrics_history: List[Dict[str, Any]]) -> float:
        if not metrics_history:
            return 0.0
        smoothed_value = metrics_history[0].get("cpu_utilization", 0.5)
        for metric in metrics_history[1:]:
            smoothed_value = self.alpha * metric.get("cpu_utilization", 0.5) + (1 - self.alpha) * smoothed_value
        return smoothed_value

class PredictiveScalingEngine:
    def __init__(self, model: PredictiveScalingModel = None):
        self.model = model or ExponentialSmoothingModel()

    async def analyze_and_recommend(self, metrics_history: List[Dict[str, Any]], current_resources: int) -> ScalingRecommendation:
        predicted_load = await self.model.predict(metrics_history)
        recommended_resources = current_resources
        reason = "No scaling needed"
        if predicted_load > 0.8:
            recommended_resources = int(current_resources * 1.5)
            reason = "High load predicted, scaling up"
        elif predicted_load < 0.3:
            recommended_resources = max(1, int(current_resources * 0.5))
            reason = "Low load predicted, scaling down"
        result = ScalingRecommendation(
            predicted_load=predicted_load,
            current_resources=current_resources,
            recommended_resources=recommended_resources,
            reason=reason
        )
        await holo_misha_instance.notify_ar(f"Scaling recommendation: {reason} - HoloMisha programs the universe!", "uk")
        await security_logger.log_security_event("system", "scaling_recommendation", {"reason": reason, "predicted_load": predicted_load})
        return result