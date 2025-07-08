import json
import time
from typing import Any, Optional, Dict

class CacheService:
    def __init__(self):
        # Simple in-memory cache for demo purposes
        # In production, you might want to use Redis
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = 3600  # 1 hour

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.
        """
        if key not in self._cache:
            return None
        
        cache_entry = self._cache[key]
        
        # Check if expired
        if time.time() > cache_entry['expires_at']:
            del self._cache[key]
            return None
        
        return cache_entry['value']

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Set value in cache with TTL.
        """
        if ttl is None:
            ttl = self.default_ttl
        
        expires_at = time.time() + ttl
        
        self._cache[key] = {
            'value': value,
            'expires_at': expires_at
        }

    def delete(self, key: str) -> bool:
        """
        Delete key from cache.
        """
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    def clear(self) -> None:
        """
        Clear all cache entries.
        """
        self._cache.clear()

    def cleanup_expired(self) -> None:
        """
        Remove expired entries from cache.
        """
        current_time = time.time()
        expired_keys = [
            key for key, entry in self._cache.items()
            if current_time > entry['expires_at']
        ]
        
        for key in expired_keys:
            del self._cache[key]

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        """
        self.cleanup_expired()
        return {
            'total_entries': len(self._cache),
            'cache_keys': list(self._cache.keys())
        }

