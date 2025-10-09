"""
Unit tests for the extended monitoring module
"""
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
import psutil
from src.monitoring.extended_monitor import ExtendedMonitor, SystemMetrics, RedisMetrics, SecurityMetrics, AIMetrics

@pytest.fixture
def extended_monitor():
    """Create a test instance of ExtendedMonitor"""
    with patch('src.monitoring.extended_monitor.redis_client'), \
         patch('src.monitoring.extended_monitor.psutil'):
        monitor = ExtendedMonitor()
        return monitor

@pytest.mark.asyncio
async def test_extended_monitor_initialization(extended_monitor):
    """Test extended monitor initialization"""
    assert extended_monitor is not None
    assert isinstance(extended_monitor.system_metrics, SystemMetrics)
    assert isinstance(extended_monitor.redis_metrics, RedisMetrics)
    assert isinstance(extended_monitor.security_metrics, SecurityMetrics)
    assert isinstance(extended_monitor.ai_metrics, AIMetrics)

@pytest.mark.asyncio
async def test_system_metrics_collection():
    """Test system metrics collection"""
    with patch('src.monitoring.extended_monitor.psutil') as mock_psutil:
        # Mock psutil responses
        mock_psutil.cpu_percent.return_value = 25.0
        mock_memory = Mock()
        mock_memory.percent = 45.0
        mock_memory.total = 8 * 1024**3  # 8GB
        mock_memory.available = 4 * 1024**3  # 4GB
        mock_memory.used = 4 * 1024**3  # 4GB
        mock_psutil.virtual_memory.return_value = mock_memory
        
        mock_disk = Mock()
        mock_disk.used = 50 * 1024**3  # 50GB
        mock_disk.total = 100 * 1024**3  # 100GB
        mock_disk.free = 50 * 1024**3  # 50GB
        mock_psutil.disk_usage.return_value = mock_disk
        
        mock_net_io = Mock()
        mock_net_io.bytes_sent = 1000000
        mock_net_io.bytes_recv = 2000000
        mock_net_io.packets_sent = 1000
        mock_net_io.packets_recv = 2000
        mock_psutil.net_io_counters.return_value = mock_net_io
        
        system_metrics = SystemMetrics()
        metrics = system_metrics.get_system_metrics()
        
        assert "cpu" in metrics
        assert "memory" in metrics
        assert "disk" in metrics
        assert "network" in metrics
        assert metrics["cpu"]["percent"] == 25.0
        assert metrics["memory"]["percent"] == 45.0

@pytest.mark.asyncio
async def test_redis_metrics_collection(extended_monitor):
    """Test Redis metrics collection"""
    with patch.object(extended_monitor.redis_metrics, 'redis_client') as mock_redis_client:
        # Mock Redis client responses
        mock_redis_client.ping = AsyncMock(return_value=True)
        mock_redis_client.cache = {}
        mock_redis_client.max_cache_size = 1000
        extended_monitor.redis_metrics.cache_hit_count = 50
        extended_monitor.redis_metrics.cache_miss_count = 10
        extended_monitor.redis_metrics.redis_error_count = 2
        
        metrics = await extended_monitor.redis_metrics.get_redis_metrics()
        
        assert "connected" in metrics
        assert "latency_ms" in metrics
        assert "cache_stats" in metrics
        assert "errors" in metrics
        assert metrics["connected"] is True
        assert metrics["errors"] == 2
        assert metrics["cache_stats"]["cache_hit_rate"] == 50 / (50 + 10)

@pytest.mark.asyncio
async def test_security_metrics_collection(extended_monitor):
    """Test security metrics collection"""
    with patch.object(extended_monitor.security_metrics, 'firewall') as mock_firewall:
        # Mock firewall attributes
        mock_firewall.threats_blocked = 5
        mock_firewall.is_active = True
        mock_firewall.threat_history = [
            {"process_id": "proc1", "threat_level": "high", "violation_type": "malicious_content"},
            {"process_id": "proc2", "threat_level": "medium", "violation_type": "invalid_input"}
        ]
        
        metrics = await extended_monitor.security_metrics.get_security_metrics()
        
        assert "firewall" in metrics
        assert "recent_threats" in metrics
        assert metrics["firewall"]["active"] is True
        assert metrics["firewall"]["threats_blocked"] == 5
        assert len(metrics["recent_threats"]) == 2

@pytest.mark.asyncio
async def test_ai_metrics_collection(extended_monitor):
    """Test AI metrics collection"""
    with patch.object(extended_monitor.ai_metrics, 'agent_guard') as mock_agent_guard:
        # Mock agent guard attributes
        mock_agent_guard.agent_states = {
            "agent1": "active",
            "agent2": "active",
            "agent3": "sleeping",
            "agent4": "error"
        }
        
        metrics = await extended_monitor.ai_metrics.get_ai_metrics()
        
        assert "total_agents" in metrics
        assert "agent_states" in metrics
        assert "active_agents" in metrics
        assert "sleeping_agents" in metrics
        assert "error_agents" in metrics
        assert metrics["total_agents"] == 4
        assert metrics["active_agents"] == 2
        assert metrics["sleeping_agents"] == 1
        assert metrics["error_agents"] == 1

@pytest.mark.asyncio
async def test_extended_monitor_get_all_metrics(extended_monitor):
    """Test extended monitor get all metrics"""
    with patch.object(extended_monitor, 'system_metrics') as mock_system_metrics, \
         patch.object(extended_monitor, 'redis_metrics') as mock_redis_metrics, \
         patch.object(extended_monitor, 'security_metrics') as mock_security_metrics, \
         patch.object(extended_monitor, 'ai_metrics') as mock_ai_metrics:
        
        # Mock all metrics methods
        mock_system_metrics.get_system_metrics.return_value = {"cpu": {"percent": 25.0}}
        mock_redis_metrics.get_redis_metrics = AsyncMock(return_value={"connected": True})
        mock_security_metrics.get_security_metrics = AsyncMock(return_value={"firewall": {"active": True}})
        mock_ai_metrics.get_ai_metrics = AsyncMock(return_value={"total_agents": 4})
        
        metrics = await extended_monitor.get_all_extended_metrics()
        
        assert "system" in metrics
        assert "redis" in metrics
        assert "security" in metrics
        assert "ai" in metrics
        assert "timestamp" in metrics
        assert metrics["system"]["cpu"]["percent"] == 25.0
        assert metrics["redis"]["connected"] is True

@pytest.mark.asyncio
async def test_health_score_calculation(extended_monitor):
    """Test health score calculation"""
    with patch.object(extended_monitor, 'get_all_extended_metrics') as mock_get_metrics:
        # Mock metrics for different health scenarios
        mock_get_metrics.return_value = {
            "system": {
                "cpu": {"percent": 25.0},
                "memory": {"percent": 45.0}
            },
            "redis": {"errors": 2}
        }
        
        health_score = await extended_monitor.get_system_health_score()
        
        assert "health_score" in health_score
        assert "status" in health_score
        assert "metrics_used" in health_score
        assert isinstance(health_score["health_score"], (int, float))
        assert 0 <= health_score["health_score"] <= 100

@pytest.mark.asyncio
async def test_health_score_with_high_cpu(extended_monitor):
    """Test health score calculation with high CPU usage"""
    with patch.object(extended_monitor, 'get_all_extended_metrics') as mock_get_metrics:
        # Mock metrics with high CPU usage
        mock_get_metrics.return_value = {
            "system": {
                "cpu": {"percent": 95.0},  # High CPU usage
                "memory": {"percent": 45.0}
            },
            "redis": {"errors": 0}
        }
        
        health_score = await extended_monitor.get_system_health_score()
        
        # With high CPU usage, health score should be lower
        assert health_score["health_score"] < 80  # Should be significantly reduced

@pytest.mark.asyncio
async def test_health_score_with_redis_errors(extended_monitor):
    """Test health score calculation with Redis errors"""
    with patch.object(extended_monitor, 'get_all_extended_metrics') as mock_get_metrics:
        # Mock metrics with Redis errors
        mock_get_metrics.return_value = {
            "system": {
                "cpu": {"percent": 25.0},
                "memory": {"percent": 45.0}
            },
            "redis": {"errors": 15}  # Many Redis errors
        }
        
        health_score = await extended_monitor.get_system_health_score()
        
        # With many Redis errors, health score should be lower
        assert health_score["health_score"] < 85  # Should be reduced

if __name__ == "__main__":
    pytest.main([__file__])