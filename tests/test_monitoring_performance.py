"""
Performance tests for monitoring enhancements
"""
import pytest
import asyncio
import time
from unittest.mock import Mock, patch, AsyncMock

# Import the modules we want to test
from src.monitoring.extended_monitor import ExtendedMonitor
from src.monitoring.api_monitor import APIMonitor

@pytest.fixture
def extended_monitor():
    """Create a test instance of ExtendedMonitor"""
    with patch('src.monitoring.extended_monitor.redis_client'), \
         patch('src.monitoring.extended_monitor.psutil'):
        monitor = ExtendedMonitor()
        return monitor

@pytest.fixture
def api_monitor():
    """Create a test instance of APIMonitor"""
    monitor = APIMonitor()
    return monitor

@pytest.mark.asyncio
async def test_extended_monitor_metrics_collection_performance(extended_monitor):
    """Test extended monitor metrics collection performance"""
    with patch.object(extended_monitor.system_metrics, 'get_system_metrics') as mock_system_metrics, \
         patch.object(extended_monitor.redis_metrics, 'get_redis_metrics') as mock_redis_metrics, \
         patch.object(extended_monitor.security_metrics, 'get_security_metrics') as mock_security_metrics, \
         patch.object(extended_monitor.ai_metrics, 'get_ai_metrics') as mock_ai_metrics:
        
        # Mock all metrics methods to return quickly
        mock_system_metrics.return_value = {"cpu": {"percent": 25.0}}
        mock_redis_metrics.return_value = {"connected": True}
        mock_security_metrics.return_value = {"firewall": {"active": True}}
        mock_ai_metrics.return_value = {"total_agents": 5}
        
        start_time = time.time()
        
        # Collect metrics multiple times
        for i in range(100):
            metrics = await extended_monitor.get_all_extended_metrics()
            assert "system" in metrics
            assert "redis" in metrics
            assert "security" in metrics
            assert "ai" in metrics
        
        end_time = time.time()
        collection_time = end_time - start_time
        
        # Metrics collection should be efficient
        assert collection_time < 2.0  # Should complete within 2 seconds

@pytest.mark.asyncio
async def test_extended_monitor_health_score_performance(extended_monitor):
    """Test extended monitor health score calculation performance"""
    with patch.object(extended_monitor, 'get_all_extended_metrics') as mock_get_metrics:
        # Mock metrics for health score calculation
        mock_get_metrics.return_value = {
            "system": {
                "cpu": {"percent": 25.0},
                "memory": {"percent": 45.0}
            },
            "redis": {"errors": 2}
        }
        
        start_time = time.time()
        
        # Calculate health score multiple times
        for i in range(100):
            health_score = await extended_monitor.get_system_health_score()
            assert "health_score" in health_score
            assert "status" in health_score
            assert isinstance(health_score["health_score"], (int, float))
        
        end_time = time.time()
        calculation_time = end_time - start_time
        
        # Health score calculation should be efficient
        assert calculation_time < 2.0  # Should complete within 2 seconds

@pytest.mark.asyncio
async def test_api_monitor_performance(api_monitor):
    """Test API monitor performance"""
    # Register multiple endpoints
    endpoints = []
    for i in range(50):
        endpoint = api_monitor.register_endpoint(f"/api/endpoint_{i}")
        endpoints.append(endpoint)
    
    start_time = time.time()
    
    # Record many requests across different endpoints
    for i in range(1000):
        endpoint_index = i % 50
        api_monitor.record_request(
            f"/api/endpoint_{endpoint_index}",
            response_time=0.1 + (i % 100) * 0.001,  # Vary response time
            status_code=200 if i % 20 != 0 else 500,  # 5% error rate
            success=i % 20 != 0
        )
    
    end_time = time.time()
    recording_time = end_time - start_time
    
    # Verify metrics
    assert api_monitor.total_requests == 1000
    assert api_monitor.total_errors == 50  # 5% of 1000
    assert len(api_monitor.endpoints) == 50
    
    # Request recording should be efficient
    assert recording_time < 1.0  # Should complete within 1 second

@pytest.mark.asyncio
async def test_api_monitor_metrics_calculation_performance(api_monitor):
    """Test API monitor metrics calculation performance"""
    # Register endpoints and record requests
    for i in range(10):
        api_monitor.register_endpoint(f"/api/test_{i}")
        
        # Record requests for each endpoint
        for j in range(100):
            api_monitor.record_request(
                f"/api/test_{i}",
                response_time=0.1 + j * 0.001,
                status_code=200,
                success=True
            )
    
    start_time = time.time()
    
    # Calculate various metrics multiple times
    for i in range(100):
        # Get overall metrics
        overall_metrics = api_monitor.get_overall_metrics()
        assert "total_requests" in overall_metrics
        assert "error_rate" in overall_metrics
        
        # Get system health
        system_health = api_monitor.get_system_health()
        assert "status" in system_health
        assert "overall_metrics" in system_health
        
        # Get top endpoints
        top_endpoints = api_monitor.get_top_endpoints_by_traffic(5)
        assert isinstance(top_endpoints, list)
    
    end_time = time.time()
    calculation_time = end_time - start_time
    
    # Metrics calculation should be efficient
    assert calculation_time < 2.0  # Should complete within 2 seconds

@pytest.mark.asyncio
async def test_api_monitor_concurrent_performance(api_monitor):
    """Test API monitor concurrent performance"""
    # Register endpoints
    for i in range(10):
        api_monitor.register_endpoint(f"/api/concurrent_{i}")
    
    async def record_requests(endpoint_index, num_requests):
        """Record requests for a specific endpoint"""
        for j in range(num_requests):
            api_monitor.record_request(
                f"/api/concurrent_{endpoint_index}",
                response_time=0.1 + j * 0.001,
                status_code=200 if j % 10 != 0 else 500,  # 10% error rate
                success=j % 10 != 0
            )
        return num_requests
    
    start_time = time.time()
    
    # Run multiple concurrent recording tasks
    tasks = [record_requests(i, 100) for i in range(10)]
    results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    concurrent_time = end_time - start_time
    
    # Verify all requests were recorded
    assert sum(results) == 1000  # 10 endpoints * 100 requests each
    assert api_monitor.total_requests == 1000
    assert api_monitor.total_errors == 100  # 10% of 1000
    
    # Concurrent operations should be efficient
    assert concurrent_time < 1.0  # Should complete within 1 second

@pytest.mark.asyncio
async def test_monitoring_data_structure_performance(extended_monitor):
    """Test monitoring data structure performance"""
    with patch.object(extended_monitor.system_metrics, 'get_system_metrics') as mock_get_metrics:
        # Mock system metrics
        mock_get_metrics.return_value = {
            "cpu": {"percent": 25.0, "avg_last_10": 22.5},
            "memory": {"percent": 45.0, "total_gb": 8.0, "available_gb": 4.0},
            "disk": {"percent": 30.0, "total_gb": 100.0, "used_gb": 30.0},
            "network": {"bytes_sent": 1000000, "bytes_recv": 2000000}
        }
        
        start_time = time.time()
        
        # Create and access large amounts of monitoring data
        metrics_history = []
        for i in range(1000):
            metrics = await extended_monitor.get_all_extended_metrics()
            metrics_history.append(metrics)
            
            # Access nested data structures
            cpu_percent = metrics["system"]["cpu"]["percent"]
            memory_percent = metrics["system"]["memory"]["percent"]
            assert cpu_percent == 25.0
            assert memory_percent == 45.0
        
        end_time = time.time()
        data_access_time = end_time - start_time
        
        # Data structure operations should be efficient
        assert len(metrics_history) == 1000
        assert data_access_time < 2.0  # Should complete within 2 seconds

@pytest.mark.asyncio
async def test_monitoring_reset_performance(api_monitor):
    """Test monitoring reset performance"""
    # Register endpoints and record many requests
    for i in range(100):
        api_monitor.register_endpoint(f"/api/reset_test_{i}")
        
        for j in range(100):
            api_monitor.record_request(
                f"/api/reset_test_{i}",
                response_time=0.1,
                status_code=200,
                success=True
            )
    
    # Verify data was recorded
    assert api_monitor.total_requests == 10000
    assert len(api_monitor.endpoints) == 100
    
    start_time = time.time()
    
    # Reset all metrics
    api_monitor.reset_metrics()
    
    end_time = time.time()
    reset_time = end_time - start_time
    
    # Verify metrics were reset
    assert api_monitor.total_requests == 0
    assert api_monitor.total_errors == 0
    assert len(api_monitor.endpoints) == 0
    
    # Reset operation should be efficient
    assert reset_time < 0.1  # Should complete very quickly

if __name__ == "__main__":
    pytest.main([__file__])