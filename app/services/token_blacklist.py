import logging
from typing import Optional
from app.core.redis import get_redis

logger = logging.getLogger(__name__)


class TokenBlacklistService:

    def __init__(self):
        self.prefix = "blacklist:"
        self.default_ttl = 604800

    async def _get_redis(self):
        return await get_redis()

    async def add_to_blacklist(
        self,
        token: str,
        user_id: str,
        ttl: Optional[int] = None,
    ) -> bool:

        redis = await self._get_redis()
        key = f"{self.prefix}{token}"
        ttl = ttl or self.default_ttl

        await redis.setex(key, ttl, user_id)
        logger.info(f"Token blacklisted for user {user_id}")

    async def is_blacklisted(
        self,
        token: str,
    ) -> bool:

        redis = await self._get_redis()
        key = f"{self.prefix}{token}"
        exists = await redis.exists(key)
        return exists > 0

    async def get_token_owner(self, token: str):
        redis = await self._get_redis()
        key = f"{self.prefix}{token}"
        return await redis.get(key)

    async def remove_from_blacklist(self, token: str) -> None:
        redis = await self._get_redis()
        key = f"{self.prefix}{token}"
        deleted = await redis.delete(key)

        if not deleted:
            logger.warning(f"Token not found in blacklist: {token[:20]}...")
