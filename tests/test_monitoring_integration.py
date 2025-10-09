"""
Integration tests for monitoring enhancements
"""
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

# Import the modules we want to test integration between
from src.monitoring.extended_monitor import ExtendedMonitor
from src.monitoring.dashboard import MonitoringDashboard
from src.monitoring.api_monitor import APIMonitor

@pytest.fixture
def extended_monitor():
    """Create a test instance of ExtendedMonitor"""
    with patch('src.monitoring.extended_monitor.redis_client'), \
         patch('src.monitoring.extended_monitor.psutil'):
        monitor = ExtendedMonitor()
        return monitor

@pytest.fixture
def monitoring_dashboard(extended_monitor):
    """Create a test instance of MonitoringDashboard"""
    with patch('src.monitoring.dashboard.api_monitor') as mock_api_monitor, \
         patch('src.monitoring.dashboard.health_check'), \
         patch('src.monitoring.dashboard.extended_monitor', extended_monitor):
        # Mock API monitor
        mock_api_monitor.total_requests = 100
        mock_api_monitor.total_errors = 5
        mock_api_monitor.active_connections = 10
        mock_api_monitor.peak_connections = 15
        mock_api_monitor.endpoints = {"test_endpoint": Mock()}
        mock_api_monitor.get_system_health.return_value = {
            "status": "healthy",
            "overall_metrics": {
                "total_requests": 100,
                "total_errors": 5,
                "error_rate": 0.05
            }
        }
        
        dashboard = MonitoringDashboard()
        return dashboard

@pytest.fixture
def api_monitor():
    """Create a test instance of APIMonitor"""
    monitor = APIMonitor()
    return monitor

@pytest.mark.asyncio
async def test_extended_monitor_system_metrics_integration(extended_monitor):
    """Test ExtendedMonitor system metrics integration"""
    with patch.object(extended_monitor.system_metrics, 'get_system_metrics') as mock_get_metrics:
        # Mock system metrics
        mock_get_metrics.return_value = {
            "cpu": {"percent": 25.0, "avg_last_10": 22.5},
            "memory": {"percent": 45.0, "total_gb": 8.0},
            "disk": {"percent": 30.0, "total_gb": 100.0},
            "network": {"bytes_sent": 1000000, "bytes_recv": 2000000}
        }
        
        metrics = await extended_monitor.get_all_extended_metrics()
        
        assert "system" in metrics
        assert metrics["system"]["cpu"]["percent"] == 25.0
        assert metrics["system"]["memory"]["percent"] == 45.0

@pytest.mark.asyncio
async def test_extended_monitor_redis_metrics_integration(extended_monitor):
    """Test ExtendedMonitor Redis metrics integration"""
    with patch.object(extended_monitor.redis_metrics, 'get_redis_metrics') as mock_get_metrics:
        # Mock Redis metrics
        mock_get_metrics.return_value = {
            "connected": True,
            "latency_ms": 5.2,
            "cache_stats": {"cache_hit_rate": 0.95, "cache_size": 50},
            "errors": 0
        }
        
        metrics = await extended_monitor.get_all_extended_metrics()
        
        assert "redis" in metrics
        assert metrics["redis"]["connected"] is True
        assert metrics["redis"]["latency_ms"] == 5.2

@pytest.mark.asyncio
async def test_extended_monitor_security_metrics_integration(extended_monitor):
    """Test ExtendedMonitor security metrics integration"""
    with patch.object(extended_monitor.security_metrics, 'get_security_metrics') as mock_get_metrics:
        # Mock security metrics
        mock_get_metrics.return_value = {
            "firewall": {"active": True, "threats_blocked": 10},
            "recent_threats": [{"type": "malicious_content", "severity": "high"}]
        }
        
        metrics = await extended_monitor.get_all_extended_metrics()
        
        assert "security" in metrics
        assert metrics["security"]["firewall"]["active"] is True
        assert metrics["security"]["firewall"]["threats_blocked"] == 10

@pytest.mark.asyncio
async def test_extended_monitor_ai_metrics_integration(extended_monitor):
    """Test ExtendedMonitor AI metrics integration"""
    with patch.object(extended_monitor.ai_metrics, 'get_ai_metrics') as mock_get_metrics:
        # Mock AI metrics
        mock_get_metrics.return_value = {
            "total_agents": 5,
            "agent_states": {"active": 3, "sleeping": 1, "error": 1},
            "active_agents": 3
        }
        
        metrics = await extended_monitor.get_all_extended_metrics()
        
        assert "ai" in metrics
        assert metrics["ai"]["total_agents"] == 5
        assert metrics["ai"]["active_agents"] == 3

@pytest.mark.asyncio
async def test_monitoring_dashboard_extended_metrics_integration(monitoring_dashboard, extended_monitor):
    """Test MonitoringDashboard integration with ExtendedMonitor"""
    with patch.object(extended_monitor, 'get_all_extended_metrics') as mock_get_metrics, \
         patch.object(extended_monitor, 'get_system_health_score') as mock_get_health_score:
        
        # Mock extended metrics
        mock_get_metrics.return_value = {
            "system": {"cpu": {"percent": 25.0}},
            "redis": {"connected": True},
            "security": {"firewall": {"active": True}},
            "ai": {"total_agents": 5}
        }
        
        # Mock health score
        mock_get_health_score.return_value = {
            "health_score": 95,
            "status": "healthy"
        }
        
        # Test getting extended system metrics
        extended_metrics = await monitoring_dashboard.get_extended_system_metrics()
        
        assert "system" in extended_metrics
        assert "redis" in extended_metrics
        assert "security" in extended_metrics
        assert "ai" in extended_metrics

@pytest.mark.asyncio
async def test_monitoring_dashboard_health_score_integration(monitoring_dashboard, extended_monitor):
    """Test MonitoringDashboard integration with health score calculation"""
    with patch.object(extended_monitor, 'get_system_health_score') as mock_get_health_score:
        # Mock health score
        mock_get_health_score.return_value = {
            "health_score": 85,
            "status": "degraded",
            "metrics_used": {"system": {"cpu": {"percent": 75.0}}}
        }
        
        # Test getting health score report
        health_report = await monitoring_dashboard.get_health_score_report()
        
        assert "health_score" in health_report
        assert health_report["health_score"]["health_score"] == 85
        assert health_report["health_score"]["status"] == "degraded"

@pytest.mark.asyncio
async def test_api_monitor_endpoint_registration(api_monitor):
    """Test APIMonitor endpoint registration"""
    # Register an endpoint
    endpoint = api_monitor.register_endpoint("/api/test")
    
    assert endpoint is not None
    assert "/api/test" in api_monitor.endpoints
    assert api_monitor.endpoints["/api/test"].endpoint_name == "/api/test"

@pytest.mark.asyncio
async def test_api_monitor_request_recording(api_monitor):
    """Test APIMonitor request recording"""
    # Register an endpoint
    endpoint = api_monitor.register_endpoint("/api/test")
    
    # Record some requests
    api_monitor.record_request("/api/test", 0.1, 200, True)  # Success
    api_monitor.record_request("/api/test", 0.2, 500, False)  # Error
    api_monitor.record_request("/api/test", 0.15, 200, True)  # Success
    
    # Check metrics
    assert api_monitor.total_requests == 3
    assert api_monitor.total_errors == 1
    assert endpoint.request_count == 3
    assert endpoint.error_count == 1
    assert endpoint.get_average_response_time() == (0.1 + 0.2 + 0.15) / 3

@pytest.mark.asyncio
async def test_api_monitor_system_health(api_monitor):
    """Test APIMonitor system health calculation"""
    # Register endpoints and record requests
    api_monitor.register_endpoint("/api/success")
    api_monitor.register_endpoint("/api/error")
    
    # Record requests with different success rates
    for i in range(100):
        if i < 95:  # 95% success rate
            api_monitor.record_request("/api/success", 0.1, 200, True)
        else:  # 5% error rate
            api_monitor.record_request("/api/error", 0.2, 500, False)
    
    # Check system health
    health = api_monitor.get_system_health()
    assert health["status"] == "healthy"  # < 1% error rate should be healthy
    assert health["overall_metrics"]["total_requests"] == 100
    assert health["overall_metrics"]["total_errors"] == 5

@pytest.mark.asyncio
async def test_monitoring_data_export_integration(monitoring_dashboard, extended_monitor):
    """Test monitoring data export integration"""
    with patch.object(monitoring_dashboard, 'get_system_overview') as mock_get_overview, \
         patch.object(monitoring_dashboard, 'get_detailed_api_metrics') as mock_get_api_metrics, \
         patch.object(monitoring_dashboard, 'get_security_report') as mock_get_security_report, \
         patch.object(monitoring_dashboard, 'get_extended_system_metrics') as mock_get_extended_metrics, \
         patch.object(monitoring_dashboard, 'get_health_score_report') as mock_get_health_score:
        
        # Mock all dashboard methods
        mock_get_overview.return_value = {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
        mock_get_api_metrics.return_value = {"endpoint_metrics": {}}
        mock_get_security_report.return_value = {"threats_blocked": 0}
        mock_get_extended_metrics.return_value = {"system": {"cpu": {"percent": 25.0}}}
        mock_get_health_score.return_value = {"health_score": {"health_score": 95}}
        
        # Test JSON export
        exported_data = await monitoring_dashboard.export_metrics("json")
        
        assert isinstance(exported_data, str)
        assert "system_overview" in exported_data
        assert "api_metrics" in exported_data
        assert "security_report" in exported_data
        assert "extended_metrics" in exported_data
        assert "health_score" in exported_data

if __name__ == "__main__":
    pytest.main([__file__])