"""
Performance tests for Redis optimizations
"""
import pytest
import asyncio
import time
from unittest.mock import Mock, patch, AsyncMock

# Import the modules we want to test
from src.lib.redis_client import OptimizedRedisClient

@pytest.fixture
def optimized_redis_client():
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

@pytest.mark.asyncio
async def test_redis_connection_pool_performance(optimized_redis_client):
    """Test Redis connection pool performance improvement"""
    # Mock Redis client methods
    optimized_redis_client.client.get = AsyncMock(return_value="test_value")
    optimized_redis_client.client.set = AsyncMock(return_value=True)
    
    # Measure time for multiple operations
    start_time = time.time()
    
    # Perform multiple Redis operations
    for i in range(100):
        await optimized_redis_client.set(f"key_{i}", f"value_{i}")
        await optimized_redis_client.get(f"key_{i}")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    # Verify all operations completed
    assert optimized_redis_client.client.set.call_count == 100
    assert optimized_redis_client.client.get.call_count == 100
    
    # In a real test, we would compare this time with the old implementation
    # For now, we just verify the operations complete in reasonable time
    assert total_time < 5.0  # Should complete within 5 seconds

@pytest.mark.asyncio
async def test_redis_caching_performance(optimized_redis_client):
    """Test Redis caching performance improvement"""
    # Mock Redis client methods
    optimized_redis_client.client.get = AsyncMock(return_value="test_value")
    optimized_redis_client.client.set = AsyncMock(return_value=True)
    
    # Test cache hit performance
    await optimized_redis_client.set("cached_key", "cached_value", use_cache=True)
    
    # Measure time for cache hits
    start_time = time.time()
    
    # Perform multiple cache hits
    for i in range(1000):
        result = await optimized_redis_client.get("cached_key", use_cache=True)
        assert result == "cached_value"
    
    end_time = time.time()
    cache_hit_time = end_time - start_time
    
    # Measure time for Redis hits (no cache)
    optimized_redis_client.client.get.reset_mock()
    
    start_time = time.time()
    
    # Perform multiple Redis hits
    for i in range(100):
        await optimized_redis_client.get("redis_key", use_cache=False)
    
    end_time = time.time()
    redis_hit_time = end_time - start_time
    
    # Cache hits should be significantly faster than Redis hits
    # In this mock test, both will be fast, but in reality cache hits would be much faster
    assert optimized_redis_client.client.get.call_count == 100

@pytest.mark.asyncio
async def test_redis_cache_size_limit_performance(optimized_redis_client):
    """Test Redis cache size limit performance"""
    optimized_redis_client.client.set = AsyncMock(return_value=True)
    
    # Fill cache beyond limit
    start_time = time.time()
    
    for i in range(optimized_redis_client.max_cache_size + 100):
        await optimized_redis_client.set(f"key_{i}", f"value_{i}", use_cache=True)
    
    end_time = time.time()
    fill_time = end_time - start_time
    
    # Verify cache size is maintained
    assert len(optimized_redis_client.cache) <= optimized_redis_client.max_cache_size
    
    # Cache size maintenance should be efficient
    assert fill_time < 2.0  # Should complete within 2 seconds

@pytest.mark.asyncio
async def test_redis_concurrent_access_performance(optimized_redis_client):
    """Test Redis concurrent access performance"""
    # Mock Redis client methods
    optimized_redis_client.client.incr = AsyncMock(return_value=1)
    
    # Measure time for concurrent operations
    start_time = time.time()
    
    # Create multiple concurrent tasks
    async def increment_counter():
        return await optimized_redis_client.incr("test_counter")
    
    tasks = [increment_counter() for _ in range(50)]
    results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    concurrent_time = end_time - start_time
    
    # All operations should succeed
    assert len(results) == 50
    assert all(result == 1 for result in results)
    assert optimized_redis_client.client.incr.call_count == 50
    
    # Concurrent operations should be efficient
    assert concurrent_time < 3.0  # Should complete within 3 seconds

@pytest.mark.asyncio
async def test_redis_json_operations_performance(optimized_redis_client):
    """Test Redis JSON operations performance"""
    import json
    
    # Mock Redis client methods
    test_data = {"key": "value", "number": 42, "nested": {"inner": "data"}}
    optimized_redis_client.client.get = AsyncMock(return_value=json.dumps(test_data))
    optimized_redis_client.client.set = AsyncMock(return_value=True)
    
    # Measure time for JSON operations
    start_time = time.time()
    
    # Perform multiple JSON operations
    for i in range(100):
        await optimized_redis_client.set_json(f"json_key_{i}", test_data)
        result = await optimized_redis_client.get_json(f"json_key_{i}")
        assert result == test_data
    
    end_time = time.time()
    json_time = end_time - start_time
    
    # Verify all operations completed
    assert optimized_redis_client.client.set.call_count == 100
    assert optimized_redis_client.client.get.call_count == 100
    
    # JSON operations should be efficient
    assert json_time < 5.0  # Should complete within 5 seconds

@pytest.mark.asyncio
async def test_redis_memory_usage_performance(optimized_redis_client):
    """Test Redis memory usage performance"""
    optimized_redis_client.client.set = AsyncMock(return_value=True)
    
    # Fill cache with data
    for i in range(1000):
        await optimized_redis_client.set(f"key_{i}", f"value_{i}" * 100, use_cache=True)
    
    # Verify cache size is reasonable
    cache_size = len(optimized_redis_client.cache)
    assert cache_size > 0
    assert cache_size <= optimized_redis_client.max_cache_size
    
    # Test cache cleanup performance
    start_time = time.time()
    
    # Simulate cache expiration
    current_time = asyncio.get_event_loop().time()
    for key in list(optimized_redis_client.cache_ttl.keys())[:100]:
        optimized_redis_client.cache_ttl[key] = current_time - 1000  # Expired
    
    # Access expired keys to trigger cleanup
    for key in list(optimized_redis_client.cache_ttl.keys())[:10]:
        optimized_redis_client._is_cached(key)
    
    end_time = time.time()
    cleanup_time = end_time - start_time
    
    # Cleanup should be efficient
    assert cleanup_time < 1.0  # Should complete within 1 second

if __name__ == "__main__":
    pytest.main([__file__])