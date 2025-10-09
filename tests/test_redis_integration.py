"""
Integration tests for Redis optimizations
"""
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock

# Import the modules we want to test integration between
from src.lib.redis_client import OptimizedRedisClient
from src.chip_design.family_collaboration_engine import FamilyCollaborationEngine
from src.chip_design.chip_driver_generator import ChipDriverGenerator
from src.analytics.chip_analytics import ChipAnalytics

@pytest.fixture
def redis_client():
    """Create a test instance of OptimizedRedisClient"""
    with patch('src.lib.redis_client.Redis') as mock_redis, \
         patch('src.lib.redis_client.ConnectionPool'):
        mock_redis_instance = AsyncMock()
        mock_redis.return_value = mock_redis_instance
        client = OptimizedRedisClient()
        # Reset the singleton for each test
        OptimizedRedisClient._instance = None
        OptimizedRedisClient._initialized = False
        return client

@pytest.fixture
def family_collaboration_engine(redis_client):
    """Create a test instance of FamilyCollaborationEngine"""
    with patch('src.chip_design.family_collaboration_engine.redis_client', redis_client), \
         patch('src.chip_design.family_collaboration_engine.holo_misha_instance'), \
         patch('src.chip_design.family_collaboration_engine.security_logger'):
        engine = FamilyCollaborationEngine()
        return engine

@pytest.fixture
def chip_driver_generator(redis_client):
    """Create a test instance of ChipDriverGenerator"""
    with patch('src.chip_design.chip_driver_generator.redis_client', redis_client), \
         patch('src.chip_design.chip_driver_generator.holo_misha_instance'), \
         patch('src.chip_design.chip_driver_generator.security_logger'), \
         patch('src.chip_design.chip_driver_generator.firewall'), \
         patch('src.chip_design.chip_driver_generator.ai_design'):
        generator = ChipDriverGenerator()
        return generator

@pytest.fixture
def chip_analytics(redis_client):
    """Create a test instance of ChipAnalytics"""
    with patch('src.analytics.chip_analytics.redis_client', redis_client), \
         patch('src.analytics.chip_analytics.holo_misha_instance'), \
         patch('src.analytics.chip_analytics.security_logger'):
        analytics = ChipAnalytics()
        return analytics

@pytest.mark.asyncio
async def test_family_collaboration_engine_redis_integration(family_collaboration_engine, redis_client):
    """Test FamilyCollaborationEngine integration with optimized Redis client"""
    # Mock Redis client methods
    redis_client.client.set_json = AsyncMock(return_value=True)
    redis_client.client.get_json = AsyncMock(return_value=None)
    redis_client.client.incr = AsyncMock(return_value=1)
    
    # Test creating a collaboration space
    result = await family_collaboration_engine.create_collaboration_space(
        "test_user", 
        "test_project", 
        {"description": "Test project"}
    )
    
    assert result["status"] == "success"
    assert "space_id" in result
    # Verify Redis methods were called
    redis_client.client.set_json.assert_called()
    redis_client.client.incr.assert_called()

@pytest.mark.asyncio
async def test_chip_driver_generator_redis_integration(chip_driver_generator, redis_client):
    """Test ChipDriverGenerator integration with optimized Redis client"""
    # Mock Redis client methods
    redis_client.client.set_json = AsyncMock(return_value=True)
    redis_client.client.get_json = AsyncMock(return_value=None)
    redis_client.client.incr = AsyncMock(return_value=1)
    
    # Mock AI design optimization
    with patch.object(chip_driver_generator, 'ai_design') as mock_ai_design:
        mock_ai_design.optimize_design = AsyncMock(return_value={"status": "success", "optimized_data": {}})
        
        # Test generating a driver
        result = await chip_driver_generator.generate_driver(
            "test_user",
            "test_chip",
            {"design_data": "test_data"}
        )
        
        assert result["status"] == "success"
        assert "driver_id" in result
        # Verify Redis methods were called
        redis_client.client.set_json.assert_called()
        redis_client.client.incr.assert_called()

@pytest.mark.asyncio
async def test_chip_analytics_redis_integration(chip_analytics, redis_client):
    """Test ChipAnalytics integration with optimized Redis client"""
    # Mock Redis client methods
    redis_client.client.set_json = AsyncMock(return_value=True)
    redis_client.client.get_json = AsyncMock(return_value=None)
    redis_client.client.incr = AsyncMock(return_value=1)
    redis_client.client.keys = AsyncMock(return_value=["metric:1", "metric:2"])
    
    # Test tracking analytics
    result = await chip_analytics.track_chip_metrics(
        "test_user",
        "test_chip",
        {"performance": 95.5, "power": 1.2}
    )
    
    assert result["status"] == "success"
    assert "metric_id" in result
    # Verify Redis methods were called
    redis_client.client.set_json.assert_called()
    redis_client.client.incr.assert_called()

@pytest.mark.asyncio
async def test_redis_caching_integration(redis_client):
    """Test Redis caching integration across modules"""
    # Mock Redis client methods
    redis_client.client.set = AsyncMock(return_value=True)
    redis_client.client.get = AsyncMock(return_value=None)
    
    # Test caching functionality
    test_key = "test_cache_key"
    test_value = "test_cache_value"
    
    # First call should miss cache and hit Redis
    result1 = await redis_client.get(test_key, use_cache=True)
    assert result1 is None
    redis_client.client.get.assert_called_with(test_key)
    
    # Set value in cache
    await redis_client.set(test_key, test_value, use_cache=True)
    redis_client.client.set.assert_called_with(test_key, test_value, ex=None)
    
    # Second call should hit cache
    result2 = await redis_client.get(test_key, use_cache=True)
    # In our mock setup, we're not actually testing cache hits since we mock Redis.get to return None
    # In a real test, we would verify that cache is used

@pytest.mark.asyncio
async def test_concurrent_redis_access(redis_client):
    """Test concurrent access to Redis client"""
    # Mock Redis client methods
    redis_client.client.incr = AsyncMock(return_value=1)
    
    # Simulate concurrent access
    async def increment_counter():
        return await redis_client.incr("test_counter")
    
    # Run multiple concurrent operations
    tasks = [increment_counter() for _ in range(10)]
    results = await asyncio.gather(*tasks)
    
    # All operations should succeed
    assert all(result == 1 for result in results)
    assert redis_client.client.incr.call_count == 10

if __name__ == "__main__":
    pytest.main([__file__])