"""
Test file for API monitoring enhancements in GlobalScope MultiFrame 11.0
This file tests the enhanced monitoring capabilities added to the API.
"""
import pytest
import asyncio
from src.monitoring.api_monitor import api_monitor, record_request, get_system_health, get_all_metrics
from src.monitoring.dashboard import dashboard

def test_api_monitor_initialization():
    """Test that API monitor is properly initialized"""
    assert api_monitor is not None
    assert api_monitor.total_requests == 0
    assert api_monitor.total_errors == 0
    assert len(api_monitor.endpoints) == 0

def test_record_request():
    """Test recording a request"""
    # Record a successful request
    record_request("/test/endpoint", 0.1, 200, True)
    
    assert api_monitor.total_requests == 1
    assert api_monitor.total_errors == 0
    assert "/test/endpoint" in api_monitor.endpoints
    
    endpoint_metrics = api_monitor.endpoints["/test/endpoint"]
    assert endpoint_metrics.request_count == 1
    assert endpoint_metrics.error_count == 0
    assert endpoint_metrics.get_average_response_time() == 0.1

def test_record_failed_request():
    """Test recording a failed request"""
    # Record a failed request
    record_request("/test/endpoint2", 0.2, 500, False)
    
    assert api_monitor.total_requests == 2
    assert api_monitor.total_errors == 1
    
    endpoint_metrics = api_monitor.endpoints["/test/endpoint2"]
    assert endpoint_metrics.request_count == 1
    assert endpoint_metrics.error_count == 1
    assert endpoint_metrics.get_error_rate() == 1.0

def test_get_system_health():
    """Test getting system health"""
    health = get_system_health()
    
    assert "status" in health
    assert "timestamp" in health
    assert "overall_metrics" in health
    assert "top_endpoints" in health
    
    # Check that overall metrics are present
    overall_metrics = health["overall_metrics"]
    assert "total_requests" in overall_metrics
    assert "total_errors" in overall_metrics
    assert "error_rate" in overall_metrics

def test_get_all_metrics():
    """Test getting all metrics"""
    metrics = get_all_metrics()
    
    assert "system_health" in metrics
    assert "endpoint_metrics" in metrics
    
    system_health = metrics["system_health"]
    assert "status" in system_health
    assert "timestamp" in system_health

@pytest.mark.asyncio
async def test_dashboard_system_overview():
    """Test dashboard system overview"""
    overview = await dashboard.get_system_overview()
    
    assert "timestamp" in overview
    assert "system_status" in overview
    assert "api_metrics" in overview
    assert "security_metrics" in overview

@pytest.mark.asyncio
async def test_dashboard_detailed_metrics():
    """Test dashboard detailed metrics"""
    metrics = await dashboard.get_detailed_api_metrics()
    
    assert "timestamp" in metrics
    assert "system_health" in metrics
    assert "endpoint_metrics" in metrics

@pytest.mark.asyncio
async def test_dashboard_security_report():
    """Test dashboard security report"""
    report = await dashboard.get_security_report()
    
    assert "timestamp" in report
    assert "threats_blocked" in report
    assert "firewall_status" in report

if __name__ == "__main__":
    # Run tests
    test_api_monitor_initialization()
    test_record_request()
    test_record_failed_request()
    test_get_system_health()
    test_get_all_metrics()
    
    # Run async tests
    asyncio.run(test_dashboard_system_overview())
    asyncio.run(test_dashboard_detailed_metrics())
    asyncio.run(test_dashboard_security_report())
    
    print("All tests passed!")