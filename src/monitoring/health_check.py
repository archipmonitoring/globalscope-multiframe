import asyncio
import logging
from typing import Dict, Any, List
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("HealthCheck")

class HealthCheck:
    def __init__(self):
        self.checks = {}
        self.status = "unknown"
        self.last_check = None
    
    def register_check(self, name: str, check_function):
        """Register a health check function"""
        self.checks[name] = check_function
        logger.info(f"Registered health check: {name}")
    
    async def run_checks(self) -> Dict[str, Any]:
        """Run all registered health checks"""
        results = {}
        passed = 0
        failed = 0
        
        for name, check_function in self.checks.items():
            try:
                result = await check_function() if asyncio.iscoroutinefunction(check_function) else check_function()
                results[name] = {
                    "status": "pass" if result else "fail",
                    "result": result
                }
                if result:
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                results[name] = {
                    "status": "fail",
                    "error": str(e)
                }
                failed += 1
                logger.error(f"Health check {name} failed: {e}")
        
        self.status = "healthy" if failed == 0 else "degraded" if passed > 0 else "unhealthy"
        self.last_check = datetime.utcnow().isoformat()
        
        return {
            "status": self.status,
            "timestamp": self.last_check,
            "passed": passed,
            "failed": failed,
            "checks": results
        }
    
    def get_status(self) -> str:
        """Get current system status"""
        return self.status
    
    def get_last_check(self) -> str:
        """Get timestamp of last check"""
        return self.last_check if self.last_check else ""

# Global health check instance
health_check = HealthCheck()

# Register CAD monitoring health check
async def cad_monitoring_health_check():
    """Health check for CAD monitoring system"""
    try:
        # Check if we have any CAD tool usage data
        from cad_monitor import get_cad_system_health
        metrics = get_cad_system_health()
        return metrics["status"] != "unhealthy"
    except Exception as e:
        logger.error(f"CAD monitoring health check failed: {e}")
        return False

health_check.register_check("cad_monitoring", cad_monitoring_health_check)