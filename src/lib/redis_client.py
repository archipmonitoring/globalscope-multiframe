"""
Optimized Redis Client for GlobalScope MultiFrame 11.0
This module provides an optimized Redis client with connection pooling and caching capabilities.
"""
import asyncio
import json
from typing import Any, Optional, Dict, List
from redis.asyncio import Redis, ConnectionPool
from src.lib.utils import get_logger

logger = get_logger("OptimizedRedisClient")

class OptimizedRedisClient:
    """Optimized Redis client with connection pooling and caching."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OptimizedRedisClient, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Prevent re-initialization
        if self._initialized:
            return
            
        try:
            # Create connection pool for better performance
            self.pool = ConnectionPool(
                host="redis-master",
                port=6379,
                db=0,
                max_connections=20,
                retry_on_timeout=True,
                socket_keepalive=True,
                socket_keepalive_options={},
                health_check_interval=30
            )
            
            # Create Redis client with connection pool
            self.client = Redis(connection_pool=self.pool, decode_responses=True)
            
            # In-memory cache for frequently accessed data
            self.cache: Dict[str, Any] = {}
            self.cache_ttl: Dict[str, float] = {}
            
            # Cache configuration
            self.default_cache_ttl = 300  # 5 minutes
            self.max_cache_size = 1000
            
            self._initialized = True
            logger.info("Optimized Redis client initialized with connection pooling")
            
        except Exception as e:
            logger.error(f"Failed to initialize optimized Redis client: {e}")
            raise
    
    async def get(self, key: str, use_cache: bool = True) -> Optional[str]:
        """Get value from Redis with optional caching."""
        try:
            # Check cache first if enabled
            if use_cache and self._is_cached(key):
                logger.debug(f"Cache hit for key: {key}")
                return self.cache[key]
            
            # Get from Redis
            value = await self.client.get(key)
            
            # Cache the result if enabled
            if use_cache and value is not None:
                self._cache_set(key, value)
                
            return value
        except Exception as e:
            logger.error(f"Error getting key {key} from Redis: {e}")
            return None
    
    async def set(self, key: str, value: str, ex: Optional[int] = None, use_cache: bool = True) -> bool:
        """Set value in Redis with optional caching."""
        try:
            # Set in Redis
            result = await self.client.set(key, value, ex=ex)
            
            # Update cache if enabled
            if use_cache and result:
                self._cache_set(key, value)
                if ex:
                    # Set cache expiration to match Redis expiration
                    self.cache_ttl[key] = asyncio.get_event_loop().time() + ex
            
            return result
        except Exception as e:
            logger.error(f"Error setting key {key} in Redis: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from Redis and cache."""
        try:
            # Delete from Redis
            result = await self.client.delete(key)
            
            # Remove from cache
            self._cache_delete(key)
            
            return result > 0
        except Exception as e:
            logger.error(f"Error deleting key {key} from Redis: {e}")
            return False
    
    async def keys(self, pattern: str) -> List[str]:
        """Get keys matching pattern."""
        try:
            return await self.client.keys(pattern)
        except Exception as e:
            logger.error(f"Error getting keys with pattern {pattern}: {e}")
            return []
    
    async def incr(self, key: str) -> int:
        """Increment counter."""
        try:
            return await self.client.incr(key)
        except Exception as e:
            logger.error(f"Error incrementing key {key}: {e}")
            return 0
    
    async def flushall(self) -> bool:
        """Flush all data."""
        try:
            result = await self.client.flushall()
            # Clear cache
            self.cache.clear()
            self.cache_ttl.clear()
            return result
        except Exception as e:
            logger.error(f"Error flushing Redis: {e}")
            return False
    
    async def ping(self) -> bool:
        """Ping Redis server."""
        try:
            return await self.client.ping()
        except Exception as e:
            logger.error(f"Error pinging Redis: {e}")
            return False
    
    async def close(self):
        """Close Redis connection."""
        try:
            await self.client.close()
            logger.info("Redis connection closed")
        except Exception as e:
            logger.error(f"Error closing Redis connection: {e}")
    
    def _is_cached(self, key: str) -> bool:
        """Check if key is cached and not expired."""
        if key not in self.cache:
            return False
        
        # Check TTL
        if key in self.cache_ttl:
            if asyncio.get_event_loop().time() > self.cache_ttl[key]:
                # Expired, remove from cache
                self._cache_delete(key)
                return False
        
        return True
    
    def _cache_set(self, key: str, value: str):
        """Set value in cache with size limit."""
        # Check cache size limit
        if len(self.cache) >= self.max_cache_size:
            # Remove oldest entries
            keys_to_remove = list(self.cache.keys())[:10]  # Remove 10 oldest entries
            for k in keys_to_remove:
                self._cache_delete(k)
        
        self.cache[key] = value
        self.cache_ttl[key] = asyncio.get_event_loop().time() + self.default_cache_ttl
    
    def _cache_delete(self, key: str):
        """Delete key from cache."""
        if key in self.cache:
            del self.cache[key]
        if key in self.cache_ttl:
            del self.cache_ttl[key]
    
    async def get_json(self, key: str, use_cache: bool = True) -> Optional[Any]:
        """Get JSON value from Redis."""
        value = await self.get(key, use_cache)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON for key {key}: {e}")
        return None
    
    async def set_json(self, key: str, value: Any, ex: Optional[int] = None, use_cache: bool = True) -> bool:
        """Set JSON value in Redis."""
        try:
            json_value = json.dumps(value)
            return await self.set(key, json_value, ex, use_cache)
        except Exception as e:
            logger.error(f"Error encoding JSON for key {key}: {e}")
            return False

# Global instance
redis_client = OptimizedRedisClient()