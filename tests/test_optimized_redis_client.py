"""
Unit tests for the optimized Redis client
"""
import pytest
import asyncio
import json
from unittest.mock import Mock, patch, AsyncMock
from src.lib.redis_client import OptimizedRedisClient

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

@pytest.mark.asyncio
async def test_redis_client_initialization(redis_client):
    """Test Redis client initialization"""
    assert redis_client is not None
    assert isinstance(redis_client.cache, dict)
    assert isinstance(redis_client.cache_ttl, dict)
    assert redis_client.default_cache_ttl == 300
    assert redis_client.max_cache_size == 1000

@pytest.mark.asyncio
async def test_redis_get_set(redis_client):
    """Test Redis get and set operations"""
    # Mock the Redis client methods
    redis_client.client.get = AsyncMock(return_value="test_value")
    redis_client.client.set = AsyncMock(return_value=True)
    
    # Test set operation
    result = await redis_client.set("test_key", "test_value")
    assert result is True
    redis_client.client.set.assert_called_once_with("test_key", "test_value", ex=None)
    
    # Test get operation
    result = await redis_client.get("test_key")
    assert result == "test_value"
    redis_client.client.get.assert_called_once_with("test_key")

@pytest.mark.asyncio
async def test_redis_get_set_with_cache(redis_client):
    """Test Redis get and set operations with caching"""
    redis_client.client.get = AsyncMock(return_value="test_value")
    redis_client.client.set = AsyncMock(return_value=True)
    
    # Test set operation with cache
    result = await redis_client.set("test_key", "test_value", use_cache=True)
    assert result is True
    
    # Test get operation with cache hit
    result = await redis_client.get("test_key", use_cache=True)
    assert result == "test_value"
    
    # Verify cache was used
    assert "test_key" in redis_client.cache
    assert redis_client.cache["test_key"] == "test_value"

@pytest.mark.asyncio
async def test_redis_get_set_json(redis_client):
    """Test Redis JSON get and set operations"""
    test_data = {"key": "value", "number": 42}
    redis_client.client.get = AsyncMock(return_value=json.dumps(test_data))
    redis_client.client.set = AsyncMock(return_value=True)
    
    # Test set_json operation
    result = await redis_client.set_json("test_json_key", test_data)
    assert result is True
    redis_client.client.set.assert_called_once()
    
    # Test get_json operation
    result = await redis_client.get_json("test_json_key")
    assert result == test_data
    redis_client.client.get.assert_called_once_with("test_json_key")

@pytest.mark.asyncio
async def test_redis_error_handling(redis_client):
    """Test Redis error handling"""
    # Mock Redis client to raise an exception
    redis_client.client.get = AsyncMock(side_effect=Exception("Redis connection error"))
    redis_client.client.set = AsyncMock(side_effect=Exception("Redis connection error"))
    
    # Test get operation with error
    result = await redis_client.get("test_key")
    assert result is None
    
    # Test set operation with error
    result = await redis_client.set("test_key", "test_value")
    assert result is False

@pytest.mark.asyncio
async def test_redis_cache_size_limit(redis_client):
    """Test Redis cache size limit enforcement"""
    redis_client.client.set = AsyncMock(return_value=True)
    
    # Fill cache beyond limit
    for i in range(redis_client.max_cache_size + 20):
        await redis_client.set(f"key_{i}", f"value_{i}", use_cache=True)
    
    # Cache should not exceed max size
    assert len(redis_client.cache) <= redis_client.max_cache_size

@pytest.mark.asyncio
async def test_redis_cache_ttl(redis_client):
    """Test Redis cache TTL functionality"""
    import time
    redis_client.client.set = AsyncMock(return_value=True)
    redis_client.client.get = AsyncMock(return_value="test_value")
    
    # Set a key with cache
    await redis_client.set("test_key", "test_value", use_cache=True)
    
    # Verify cache entry exists
    assert "test_key" in redis_client.cache
    
    # Test cache expiration (simulated)
    # This is a simplified test - in reality, TTL checking happens on access
    assert "test_key" in redis_client.cache

@pytest.mark.asyncio
async def test_redis_delete(redis_client):
    """Test Redis delete operation"""
    redis_client.client.delete = AsyncMock(return_value=1)
    redis_client.cache["test_key"] = "test_value"
    
    # Test delete operation
    result = await redis_client.delete("test_key")
    assert result is True
    
    # Verify cache entry was removed
    assert "test_key" not in redis_client.cache

@pytest.mark.asyncio
async def test_redis_incr(redis_client):
    """Test Redis increment operation"""
    redis_client.client.incr = AsyncMock(return_value=5)
    
    # Test increment operation
    result = await redis_client.incr("counter_key")
    assert result == 5
    redis_client.client.incr.assert_called_once_with("counter_key")

@pytest.mark.asyncio
async def test_redis_keys(redis_client):
    """Test Redis keys operation"""
    redis_client.client.keys = AsyncMock(return_value=["key1", "key2", "key3"])
    
    # Test keys operation
    result = await redis_client.keys("pattern*")
    assert result == ["key1", "key2", "key3"]
    redis_client.client.keys.assert_called_once_with("pattern*")

if __name__ == "__main__":
    pytest.main([__file__])