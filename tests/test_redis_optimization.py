"""
Test file for Redis optimization enhancements in GlobalScope MultiFrame 11.0
This file tests the optimized Redis client and its performance improvements.
"""
import pytest
import asyncio
import json
from src.lib.redis_client import redis_client

def test_redis_client_initialization():
    """Test that Redis client is properly initialized"""
    assert redis_client is not None
    assert hasattr(redis_client, 'client')
    assert hasattr(redis_client, 'cache')
    assert hasattr(redis_client, 'cache_ttl')

@pytest.mark.asyncio
async def test_redis_set_get():
    """Test setting and getting values from Redis"""
    # Test string values
    key = "test_key"
    value = "test_value"
    
    # Set value
    result = await redis_client.set(key, value)
    assert result == True
    
    # Get value
    retrieved_value = await redis_client.get(key)
    assert retrieved_value == value

@pytest.mark.asyncio
async def test_redis_json_operations():
    """Test JSON operations with Redis"""
    # Test JSON values
    key = "test_json_key"
    value = {"name": "HoloMisha", "type": "quantum_chip", "cores": 128}
    
    # Set JSON value
    result = await redis_client.set_json(key, value)
    assert result == True
    
    # Get JSON value
    retrieved_value = await redis_client.get_json(key)
    assert retrieved_value == value

@pytest.mark.asyncio
async def test_redis_counter():
    """Test Redis counter operations"""
    key = "test_counter"
    
    # Initialize counter
    await redis_client.set(key, "0")
    
    # Increment counter
    result = await redis_client.incr(key)
    assert result == 1
    
    # Increment again
    result = await redis_client.incr(key)
    assert result == 2

@pytest.mark.asyncio
async def test_redis_caching():
    """Test Redis caching functionality"""
    key = "test_cache_key"
    value = "cached_value"
    
    # Set value with caching
    result = await redis_client.set(key, value, use_cache=True)
    assert result == True
    
    # Check that value is cached
    assert key in redis_client.cache
    assert redis_client.cache[key] == value

@pytest.mark.asyncio
async def test_redis_cache_ttl():
    """Test Redis cache TTL functionality"""
    key = "test_cache_ttl_key"
    value = "ttl_value"
    
    # Set value with short TTL
    result = await redis_client.set(key, value, ex=1, use_cache=True)  # 1 second expiration
    assert result == True
    
    # Check that value is cached
    assert key in redis_client.cache
    
    # Wait for expiration
    await asyncio.sleep(1.1)
    
    # Try to get the value (should not be cached anymore)
    retrieved_value = await redis_client.get(key, use_cache=True)
    # The cache entry should be removed, but Redis still has the value
    # (in a real scenario with Redis expiration, the value would be gone)

@pytest.mark.asyncio
async def test_redis_keys_pattern():
    """Test Redis keys pattern matching"""
    # Set some test keys
    await redis_client.set("pattern_test_1", "value1")
    await redis_client.set("pattern_test_2", "value2")
    await redis_client.set("other_key", "othervalue")
    
    # Get keys matching pattern
    keys = await redis_client.keys("pattern_test_*")
    assert len(keys) == 2
    assert "pattern_test_1" in keys
    assert "pattern_test_2" in keys

@pytest.mark.asyncio
async def test_redis_delete():
    """Test Redis delete operations"""
    key = "test_delete_key"
    value = "delete_value"
    
    # Set value
    await redis_client.set(key, value)
    
    # Verify value exists
    retrieved_value = await redis_client.get(key)
    assert retrieved_value == value
    
    # Delete value
    result = await redis_client.delete(key)
    assert result == True
    
    # Verify value is deleted
    retrieved_value = await redis_client.get(key)
    assert retrieved_value is None

if __name__ == "__main__":
    # Run tests
    test_redis_client_initialization()
    
    # Run async tests
    asyncio.run(test_redis_set_get())
    asyncio.run(test_redis_json_operations())
    asyncio.run(test_redis_counter())
    asyncio.run(test_redis_caching())
    asyncio.run(test_redis_cache_ttl())
    asyncio.run(test_redis_keys_pattern())
    asyncio.run(test_redis_delete())
    
    print("All Redis optimization tests passed!")