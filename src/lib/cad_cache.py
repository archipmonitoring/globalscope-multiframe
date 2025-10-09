import hashlib
import json
from typing import Dict, Any, Optional
import asyncio

class CADCaching:
    """Caching system for CAD tool results to optimize repeated runs"""
    
    def __init__(self, redis_client):
        self.redis_client = redis_client
        self.cache_prefix = "cad_cache:"
        self.cache_ttl = 86400  # 24 hours by default
    
    async def _generate_cache_key(self, tool_name: str, params: Dict[str, Any]) -> str:
        """Generate a unique cache key based on tool name and parameters"""
        # Create a string representation of the parameters
        params_str = json.dumps(params, sort_keys=True, separators=(',', ':'))
        # Combine tool name and parameters
        combined = f"{tool_name}:{params_str}"
        # Generate MD5 hash
        return self.cache_prefix + hashlib.md5(combined.encode()).hexdigest()
    
    async def get_cached_result(self, tool_name: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get cached result if it exists and is valid"""
        cache_key = await self._generate_cache_key(tool_name, params)
        try:
            result = await self.redis_client.get_json(cache_key)
            if result:
                # Update access time for LRU eviction
                await self.redis_client.expire(cache_key, self.cache_ttl)
                return result
        except Exception as e:
            print(f"Error getting cached result: {e}")
        return None
    
    async def cache_result(self, tool_name: str, params: Dict[str, Any], result: Dict[str, Any]):
        """Cache the result of a CAD tool operation"""
        cache_key = await self._generate_cache_key(tool_name, params)
        try:
            await self.redis_client.set_json(cache_key, result, ex=self.cache_ttl)
        except Exception as e:
            print(f"Error caching result: {e}")
    
    async def invalidate_cache(self, tool_name: Optional[str] = None, project_id: Optional[str] = None):
        """Invalidate cache entries
        
        Args:
            tool_name: Name of the CAD tool to invalidate (optional)
            project_id: Project ID to invalidate (optional)
            
        Examples:
            # Invalidate specific tool and project
            await cache.invalidate_cache("verilator", "proj_123")
            
            # Invalidate all results for a specific tool
            await cache.invalidate_cache("verilator")
            
            # Clear all cache (use with caution!)
            await cache.invalidate_cache()
        """
        if tool_name and project_id:
            # Invalidate specific tool and project
            params = {"project_id": project_id}
            cache_key = await self._generate_cache_key(tool_name, params)
            await self.redis_client.delete(cache_key)
        elif tool_name:
            # Invalidate all results for a specific tool
            # Use Redis KEYS command with pattern matching
            pattern = f"{self.cache_prefix}{tool_name}:*"
            try:
                # Get all keys matching the pattern
                keys = await self.redis_client.keys(pattern)
                if keys:
                    # Delete all matching keys
                    await self.redis_client.delete(*keys)
            except Exception as e:
                print(f"Error invalidating cache by pattern {pattern}: {e}")
        else:
            # Clear all cache - use with caution!
            try:
                await self.redis_client.flushdb()
            except Exception as e:
                print(f"Error clearing all cache: {e}")
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get statistics about the cache usage"""
        # In a real implementation, this would query Redis for info about memory usage, hit/miss ratio, etc.
        # For now, return a placeholder
        return {
            "cache_enabled": True,
            "default_ttl": self.cache_ttl,
            "cache_prefix": self.cache_prefix
        }

# Global instance will be created when imported
_cad_cache = None
def get_cad_cache():
    """Get the global CADCaching instance
    
    Returns:
        CADCaching: The global caching instance
    """
    global _cad_cache
    return _cad_cache

async def init_cad_cache(redis_client):
    """Initialize the global CADCaching instance
    
    Args:
        redis_client: Redis client instance
        
    Returns:
        CADCaching: Initialized caching instance
    """
    global _cad_cache
    _cad_cache = CADCaching(redis_client)
    return _cad_cache