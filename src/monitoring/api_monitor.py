"""
API Monitoring Module for GlobalScope MultiFrame 11.0
This module provides comprehensive monitoring and metrics tracking for API endpoints.
"""
import time
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from collections import defaultdict, deque
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("APIMonitor")

class EndpointMetrics:
    """Metrics tracking for individual API endpoints"""
    
    def __init__(self, endpoint_name: str):
        self.endpoint_name = endpoint_name
        self.request_count = 0
        self.error_count = 0
        self.total_response_time = 0.0
        self.response_times = deque(maxlen=1000)  # Keep last 1000 response times
        self.status_codes = defaultdict(int)
        self.created_at = datetime.utcnow()
    
    def record_request(self, response_time: float, status_code: int = 200, success: bool = True):
        """Record a request to this endpoint"""
        self.request_count += 1
        self.total_response_time += response_time
        self.response_times.append(response_time)
        
        if not success:
            self.error_count += 1
            
        self.status_codes[status_code] += 1
    
    def get_average_response_time(self) -> float:
        """Get average response time for this endpoint"""
        if self.request_count == 0:
            return 0.0
        return self.total_response_time / self.request_count
    
    def get_error_rate(self) -> float:
        """Get error rate for this endpoint"""
        if self.request_count == 0:
            return 0.0
        return self.error_count / self.request_count
    
    def get_recent_response_times(self, count: int = 10) -> List[float]:
        """Get recent response times"""
        return list(self.response_times)[-count:]
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get a summary of metrics for this endpoint"""
        return {
            "endpoint_name": self.endpoint_name,
            "request_count": self.request_count,
            "error_count": self.error_count,
            "error_rate": self.get_error_rate(),
            "average_response_time": self.get_average_response_time(),
            "total_response_time": self.total_response_time,
            "status_codes": dict(self.status_codes),
            "recent_response_times": self.get_recent_response_times(10),
            "created_at": self.created_at.isoformat()
        }

class APIMonitor:
    """Main API monitoring class"""
    
    def __init__(self):
        self.endpoints: Dict[str, EndpointMetrics] = {}
        self.total_requests = 0
        self.total_errors = 0
        self.start_time = datetime.utcnow()
        self.active_connections = 0
        self.peak_connections = 0
    
    def register_endpoint(self, endpoint_name: str) -> EndpointMetrics:
        """Register a new endpoint for monitoring"""
        if endpoint_name not in self.endpoints:
            self.endpoints[endpoint_name] = EndpointMetrics(endpoint_name)
            logger.info(f"Registered endpoint for monitoring: {endpoint_name}")
        return self.endpoints[endpoint_name]
    
    def record_request(self, endpoint_name: str, response_time: float, status_code: int = 200, success: bool = True):
        """Record a request to an endpoint"""
        self.total_requests += 1
        
        if not success:
            self.total_errors += 1
        
        # Register endpoint if not already registered
        if endpoint_name not in self.endpoints:
            self.register_endpoint(endpoint_name)
        
        # Record metrics for the endpoint
        self.endpoints[endpoint_name].record_request(response_time, status_code, success)
    
    def increment_connections(self):
        """Increment active connections count"""
        self.active_connections += 1
        if self.active_connections > self.peak_connections:
            self.peak_connections = self.active_connections
    
    def decrement_connections(self):
        """Decrement active connections count"""
        self.active_connections = max(0, self.active_connections - 1)
    
    def get_overall_metrics(self) -> Dict[str, Any]:
        """Get overall API metrics"""
        uptime = (datetime.utcnow() - self.start_time).total_seconds()
        
        return {
            "total_requests": self.total_requests,
            "total_errors": self.total_errors,
            "error_rate": self.total_errors / self.total_requests if self.total_requests > 0 else 0.0,
            "uptime_seconds": uptime,
            "active_connections": self.active_connections,
            "peak_connections": self.peak_connections,
            "endpoints_count": len(self.endpoints)
        }
    
    def get_endpoint_metrics(self, endpoint_name: str) -> Optional[Dict[str, Any]]:
        """Get metrics for a specific endpoint"""
        if endpoint_name in self.endpoints:
            return self.endpoints[endpoint_name].get_metrics_summary()
        return None
    
    def get_all_endpoint_metrics(self) -> Dict[str, Dict[str, Any]]:
        """Get metrics for all endpoints"""
        return {name: endpoint.get_metrics_summary() for name, endpoint in self.endpoints.items()}
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health metrics"""
        overall_metrics = self.get_overall_metrics()
        error_rate = overall_metrics["error_rate"]
        
        # Determine health status based on error rate
        if error_rate < 0.01:  # Less than 1% error rate
            health_status = "healthy"
        elif error_rate < 0.05:  # Less than 5% error rate
            health_status = "degraded"
        else:
            health_status = "unhealthy"
        
        return {
            "status": health_status,
            "timestamp": datetime.utcnow().isoformat(),
            "overall_metrics": overall_metrics,
            "top_endpoints": self.get_top_endpoints_by_traffic(5)
        }
    
    def get_top_endpoints_by_traffic(self, count: int = 5) -> List[Dict[str, Any]]:
        """Get top endpoints by request count"""
        sorted_endpoints = sorted(
            self.endpoints.items(), 
            key=lambda x: x[1].request_count, 
            reverse=True
        )
        return [
            {
                "endpoint": name,
                "requests": endpoint.request_count,
                "errors": endpoint.error_count,
                "error_rate": endpoint.get_error_rate(),
                "avg_response_time": endpoint.get_average_response_time()
            }
            for name, endpoint in sorted_endpoints[:count]
        ]
    
    def reset_metrics(self):
        """Reset all metrics (useful for testing)"""
        self.total_requests = 0
        self.total_errors = 0
        self.start_time = datetime.utcnow()
        self.active_connections = 0
        self.peak_connections = 0
        self.endpoints.clear()

# Global API monitor instance
api_monitor = APIMonitor()

# Convenience functions
def record_request(endpoint_name: str, response_time: float, status_code: int = 200, success: bool = True):
    """Record a request to an endpoint"""
    api_monitor.record_request(endpoint_name, response_time, status_code, success)

def get_system_health() -> Dict[str, Any]:
    """Get overall system health"""
    return api_monitor.get_system_health()

def get_endpoint_metrics(endpoint_name: str) -> Optional[Dict[str, Any]]:
    """Get metrics for a specific endpoint"""
    return api_monitor.get_endpoint_metrics(endpoint_name)

def get_all_metrics() -> Dict[str, Any]:
    """Get all API metrics"""
    return {
        "system_health": api_monitor.get_system_health(),
        "endpoint_metrics": api_monitor.get_all_endpoint_metrics()
    }