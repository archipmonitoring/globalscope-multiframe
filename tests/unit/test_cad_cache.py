"""
Unit tests for CAD cache functionality
"""
import pytest
import asyncio
import hashlib
import json
from unittest.mock import Mock, AsyncMock

# Import our modules
from src.lib.cad_cache import CADCaching, init_cad_cache, get_cad_cache

class TestCADCaching:
    @pytest.fixture
    def mock_redis_client(self):
        """Create a mock Redis client"""
        return AsyncMock()
    
    @pytest.fixture
    def cad_cache(self, mock_redis_client):
        """Create a CADCaching instance with mock Redis client"""
        return CADCaching(mock_redis_client)
    
    def test_init(self, mock_redis_client):
        """Test CADCaching initialization"""
        cache = CADCaching(mock_redis_client)
        assert cache.redis_client == mock_redis_client
        assert cache.cache_prefix == "cad_cache:"
        assert cache.cache_ttl == 86400
    
    def test_generate_cache_key(self, cad_cache):
        """Test cache key generation"""
        tool_name = "verilator"
        params = {"input": "test.v", "top": "top_module"}
        
        # Generate key
        key = asyncio.run(cad_cache._generate_cache_key(tool_name, params))
        
        # Verify key format
        assert key.startswith(cad_cache.cache_prefix)
        
        # Verify key is based on tool name and params
        expected_content = f"{tool_name}:{json.dumps(params, sort_keys=True, separators=(',', ':'))}"
        expected_key = cad_cache.cache_prefix + hashlib.md5(expected_content.encode()).hexdigest()
        assert key == expected_key
    
    async def test_get_cached_result_found(self, cad_cache, mock_redis_client):
        """Test getting cached result when it exists"""
        # Setup mock
        mock_result = {"output": "test output", "status": "success"}
        mock_redis_client.get_json.return_value = mock_result
        
        # Test
        result = await cad_cache.get_cached_result("verilator", {"input": "test.v"})
        
        # Verify
        assert result == mock_result
        mock_redis_client.get_json.assert_called_once()
        mock_redis_client.expire.assert_called_once()
    
    async def test_get_cached_result_not_found(self, cad_cache, mock_redis_client):
        """Test getting cached result when it doesn't exist"""
        # Setup mock
        mock_redis_client.get_json.return_value = None
        
        # Test
        result = await cad_cache.get_cached_result("verilator", {"input": "test.v"})
        
        # Verify
        assert result is None
        mock_redis_client.get_json.assert_called_once()
        mock_redis_client.expire.assert_not_called()
    
    async def test_get_cached_result_error(self, cad_cache, mock_redis_client):
        """Test getting cached result when Redis throws an error"""
        # Setup mock
        mock_redis_client.get_json.side_effect = Exception("Redis error")
        
        # Test
        result = await cad_cache.get_cached_result("verilator", {"input": "test.v"})
        
        # Verify
        assert result is None
        mock_redis_client.get_json.assert_called_once()
    
    async def test_cache_result(self, cad_cache, mock_redis_client):
        """Test caching a result"""
        # Test data
        tool_name = "verilator"
        params = {"input": "test.v"}
        result = {"output": "test output", "status": "success"}
        
        # Test
        await cad_cache.cache_result(tool_name, params, result)
        
        # Verify
        mock_redis_client.set_json.assert_called_once()
        call_args = mock_redis_client.set_json.call_args
        assert call_args[0][0].startswith(cad_cache.cache_prefix)  # cache key
        assert call_args[0][1] == result  # cached data
        assert call_args[1]['ex'] == cad_cache.cache_ttl  # TTL
    
    async def test_cache_result_error(self, cad_cache, mock_redis_client):
        """Test caching a result when Redis throws an error"""
        # Setup mock
        mock_redis_client.set_json.side_effect = Exception("Redis error")
        
        # Test (should not raise exception)
        await cad_cache.cache_result("verilator", {"input": "test.v"}, {"output": "test"})
        
        # Verify
        mock_redis_client.set_json.assert_called_once()
    
    async def test_invalidate_cache_specific(self, cad_cache, mock_redis_client):
        """Test invalidating specific cache entry"""
        # Test
        await cad_cache.invalidate_cache("verilator", "proj_123")
        
        # Verify
        mock_redis_client.delete.assert_called_once()
        call_args = mock_redis_client.delete.call_args
        assert call_args[0][0].startswith(cad_cache.cache_prefix)
    
    async def test_get_cache_stats(self, cad_cache):
        """Test getting cache statistics"""
        # Test
        stats = await cad_cache.get_cache_stats()
        
        # Verify
        assert isinstance(stats, dict)
        assert "cache_enabled" in stats
        assert "default_ttl" in stats
        assert "cache_prefix" in stats
        assert stats["cache_enabled"] == True
        assert stats["default_ttl"] == cad_cache.cache_ttl
        assert stats["cache_prefix"] == cad_cache.cache_prefix
    
    async def test_init_and_get_cad_cache(self):
        """Test initializing and getting the global cache instance"""
        # Initialize
        mock_redis = AsyncMock()
        cache = await init_cad_cache(mock_redis)
        
        # Verify initialization
        assert isinstance(cache, CADCaching)
        assert cache.redis_client == mock_redis
        
        # Verify global instance
        global_cache = get_cad_cache()
        assert global_cache is cache

if __name__ == "__main__":
    pytest.main([__file__])