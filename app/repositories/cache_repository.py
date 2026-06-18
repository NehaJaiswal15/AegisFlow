import json
import hashlib
from typing import Optional

from app.core.redis_client import redis_client


class CacheRepository:
    """Handles caching moderation results in Redis."""

    CACHE_TTL = 3600  # Cache expires after 1 hour (in seconds)
    KEY_PREFIX = "moderation:"

    @staticmethod
    def _hash_text(text: str) -> str:
        """Create a unique cache key from the text."""
        return hashlib.sha256(text.encode()).hexdigest()

    def get(self, text: str) -> Optional[dict]:
        """Check if we've seen this exact text before."""
        key = f"{self.KEY_PREFIX}{self._hash_text(text)}"
        cached = redis_client.get(key)

        if cached:
            print(f"CACHE HIT for text hash: {key[:30]}...")
            return json.loads(cached)

        print(f"CACHE MISS for text hash: {key[:30]}...")
        return None

    def save(self, text: str, result: dict):
        """Cache a moderation result for future lookups."""
        key = f"{self.KEY_PREFIX}{self._hash_text(text)}"
        redis_client.setex(
            key,
            self.CACHE_TTL,
            json.dumps(result),
        )

    def invalidate(self, text: str):
        """Remove a specific cache entry."""
        key = f"{self.KEY_PREFIX}{self._hash_text(text)}"
        redis_client.delete(key)

    def clear_all(self):
        """Clear all cached moderation results."""
        keys = redis_client.keys(f"{self.KEY_PREFIX}*")
        if keys:
            redis_client.delete(*keys)


cache_repo = CacheRepository()
