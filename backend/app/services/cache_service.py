import redis
import json
import asyncio
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from app.config import settings

class CacheService:
    def __init__(self):
        self.redis_client = None
        self._memory_cache: Dict[str, Dict[str, Any]] = {}
        
        # Try to connect to Redis
        try:
            self.redis_client = redis.from_url(settings.redis_url, decode_responses=True)
            # Test connection
            self.redis_client.ping()
        except (redis.RedisError, ConnectionError):
            print("Redis not available, falling back to in-memory cache")
            self.redis_client = None
    
    async def get(self, key: str) -> Optional[str]:
        """Get a value from cache."""
        if self.redis_client:
            try:
                return self.redis_client.get(key)
            except redis.RedisError:
                pass
        
        # Fallback to memory cache
        if key in self._memory_cache:
            cache_entry = self._memory_cache[key]
            if datetime.now() < cache_entry['expires']:
                return cache_entry['value']
            else:
                # Expired, remove from cache
                del self._memory_cache[key]
        
        return None
    
    async def set(self, key: str, value: str, expire: int = 300) -> bool:
        """Set a value in cache with expiration."""
        if self.redis_client:
            try:
                return self.redis_client.setex(key, expire, value)
            except redis.RedisError:
                pass
        
        # Fallback to memory cache
        expires_at = datetime.now() + timedelta(seconds=expire)
        self._memory_cache[key] = {
            'value': value,
            'expires': expires_at
        }
        return True
    
    async def delete(self, key: str) -> bool:
        """Delete a value from cache."""
        if self.redis_client:
            try:
                return bool(self.redis_client.delete(key))
            except redis.RedisError:
                pass
        
        # Fallback to memory cache
        if key in self._memory_cache:
            del self._memory_cache[key]
            return True
        return False
    
    async def clear_expired(self):
        """Clear expired entries from memory cache."""
        current_time = datetime.now()
        expired_keys = [
            key for key, entry in self._memory_cache.items()
            if current_time >= entry['expires']
        ]
        
        for key in expired_keys:
            del self._memory_cache[key] 