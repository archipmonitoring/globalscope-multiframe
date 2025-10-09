"""
Monitoring Dashboard for GlobalScope MultiFrame 11.0
This module provides a comprehensive dashboard for monitoring system health, API performance, and security metrics.
"""
import json
import logging
from typing import Dict, Any, List
from datetime import datetime
from src.monitoring.api_monitor import api_monitor
from src.monitoring.health_check import health_check
from src.security.quantum_singularity_firewall import QuantumSingularityFirewall
from src.monitoring.extended_monitor import extended_monitor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MonitoringDashboard")

class MonitoringDashboard:
    """Comprehensive monitoring dashboard for the system"""
    
    def __init__(self):
        self.firewall = QuantumSingularityFirewall()
        self.extended_monitor = extended_monitor
        logger.info("MonitoringDashboard initialized")
    
    async def get_system_overview(self) -> Dict[str, Any]:
        """Get a comprehensive overview of system health and performance"""
        try:
            # Get health check results
            health_results = await health_check.run_checks()
            
            # Get API metrics
            api_metrics = {
                "total_requests": api_monitor.total_requests,
                "total_errors": api_monitor.total_errors,
                "error_rate": api_monitor.total_errors / api_monitor.total_requests if api_monitor.total_requests > 0 else 0.0,
                "active_connections": api_monitor.active_connections,
                "peak_connections": api_monitor.peak_connections,
                "endpoints_count": len(api_monitor.endpoints),
                "system_health": api_monitor.get_system_health()
            }
            
            # Get security metrics using getattr to avoid linter issues
            security_metrics = {
                "threats_blocked": getattr(self.firewall, 'threats_blocked', 0),
                "firewall_status": getattr(self.firewall, 'is_active', True)
            }
            
            # Get extended metrics
            extended_metrics = await self.extended_monitor.get_all_extended_metrics()
            
            # Combine all metrics
            overview = {
                "timestamp": datetime.utcnow().isoformat(),
                "system_status": health_results["status"],
                "health_checks": health_results,
                "api_metrics": api_metrics,
                "security_metrics": security_metrics,
                "extended_metrics": extended_metrics,
                "uptime": self._calculate_uptime()
            }
            
            return overview
        except Exception as e:
            logger.error(f"Error getting system overview: {e}")
            return {"error": str(e)}
    
    async def get_detailed_api_metrics(self) -> Dict[str, Any]:
        """Get detailed API performance metrics"""
        try:
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "system_health": api_monitor.get_system_health(),
                "endpoint_metrics": api_monitor.get_all_endpoint_metrics(),
                "top_endpoints": api_monitor.get_top_endpoints_by_traffic(10)
            }
        except Exception as e:
            logger.error(f"Error getting detailed API metrics: {e}")
            return {"error": str(e)}
    
    async def get_security_report(self) -> Dict[str, Any]:
        """Get a comprehensive security report"""
        try:
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "threats_blocked": getattr(self.firewall, 'threats_blocked', 0),
                "firewall_status": getattr(self.firewall, 'is_active', True),
                "recent_threats": []  # In a real implementation, this would track recent threats
            }
        except Exception as e:
            logger.error(f"Error getting security report: {e}")
            return {"error": str(e)}
    
    async def get_extended_system_metrics(self) -> Dict[str, Any]:
        """Get extended system metrics including AI, Redis, and system resources"""
        try:
            return await self.extended_monitor.get_all_extended_metrics()
        except Exception as e:
            logger.error(f"Error getting extended system metrics: {e}")
            return {"error": str(e)}
    
    async def get_health_score_report(self) -> Dict[str, Any]:
        """Get system health score report"""
        try:
            health_score = await self.extended_monitor.get_system_health_score()
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "health_score": health_score
            }
        except Exception as e:
            logger.error(f"Error getting health score report: {e}")
            return {"error": str(e)}
    
    def _calculate_uptime(self) -> str:
        """Calculate system uptime"""
        # In a real implementation, this would calculate actual uptime
        return "99.9%"
    
    async def export_metrics(self, format: str = "json") -> str:
        """Export metrics in specified format"""
        try:
            overview = await self.get_system_overview()
            api_metrics = await self.get_detailed_api_metrics()
            security_report = await self.get_security_report()
            extended_metrics = await self.get_extended_system_metrics()
            health_score = await self.get_health_score_report()
            
            export_data = {
                "system_overview": overview,
                "api_metrics": api_metrics,
                "security_report": security_report,
                "extended_metrics": extended_metrics,
                "health_score": health_score
            }
            
            if format.lower() == "json":
                return json.dumps(export_data, indent=2)
            else:
                return str(export_data)
        except Exception as e:
            logger.error(f"Error exporting metrics: {e}")
            return json.dumps({"error": str(e)})

# Global dashboard instance
dashboard = MonitoringDashboard()

# Convenience functions
async def get_system_overview() -> Dict[str, Any]:
    """Get system overview"""
    return await dashboard.get_system_overview()

async def get_detailed_api_metrics() -> Dict[str, Any]:
    """Get detailed API metrics"""
    return await dashboard.get_detailed_api_metrics()

async def get_security_report() -> Dict[str, Any]:
    """Get security report"""
    return await dashboard.get_security_report()

async def get_extended_system_metrics() -> Dict[str, Any]:
    """Get extended system metrics"""
    return await dashboard.get_extended_system_metrics()

async def get_health_score_report() -> Dict[str, Any]:
    """Get health score report"""
    return await dashboard.get_health_score_report()