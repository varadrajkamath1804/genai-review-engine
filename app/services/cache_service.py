import json
import hashlib
import logging
from typing import Optional, Dict, Any
from app.core.redis import get_redis

logger = logging.getLogger(__name__)


class CacheService:
    def __init__(self):
        self.default_ttl = 86400
        self.prefix = "ai:cache:"

    async def _get_redis(self):
        return await get_redis()

    def _generate_key(self, text: str, context: Optional[str] = None) -> str:

        # Combine text and context
        content = f"{text}:{context or ''}"

        # Create hash (shorter key)
        hash_obj = hashlib.sha256(content.encode())
        hash_hex = hash_obj.hexdigest()[:32]  # Take first 32 chars

        return f"{self.prefix}{hash_hex}"

    async def get(self, text: str, context: Optional[str] = None) -> Optional[Dict]:
        try:
            redis = await self._get_redis()
            key = self._generate_key(text, context)

            cached = await redis.get(key)
            if cached:
                logger.info(f"✅ Cache hit for key: {key[:20]}...")
                return json.loads(cached)

            logger.info(f"❌ Cache miss for key: {key[:20]}...")
            return None

        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None

    async def set(
        self,
        text: str,
        response: Dict,
        context: Optional[str] = None,
        ttl: Optional[int] = None,
    ) -> bool:

        try:
            redis = await self._get_redis()
            key = self._generate_key(text, context)
            ttl = ttl or self.default_ttl

            await redis.setex(key, ttl, json.dumps(response))
            logger.info(f"✅ Cached response for key: {key[:20]}...")
            return True

        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False

    async def invalidate(self, text: str, context: Optional[str] = None) -> bool:

        try:
            redis = await self._get_redis()
            key = self._generate_key(text, context)

            await redis.delete(key)
            logger.info(f"🗑️ Invalidated cache for key: {key[:20]}...")
            return True

        except Exception as e:
            logger.error(f"Cache invalidation error: {e}")
            return False
