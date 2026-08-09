import json
import uuid
import logging

from redis.asyncio import Redis
from app.core.config import Settings

logger = logging.getLogger(__name__)


class CacheService:
    def __init__(
        self,
        redis: Redis,
        settings: Settings,
    ):
        self.redis = redis
        self.settings = settings

    async def get(self, key: str) -> dict | None:
        value = await self.redis.get(key)

        if value is None:
            return None
        return json.loads(value)

    async def set(
        self,
        key: str,
        value: dict,
    ) -> None:
        await self.redis.set(
            key,
            json.dumps(value),
            ex=self.settings.REDIS_CACHE_TTL,
        )

    async def invalidate(
        self,
        key: str,
    ) -> None:
        await self.redis.delete(key)

    async def acquire_lock(
        self,
        key: str,
        ttl: int = 30,
    ) -> str | None:
        lock_value = str(uuid.uuid4())
        acquired = await self.redis.set(
            key,
            lock_value,
            nx=True,
            ex=self.settings.REDIS_LOCK_TTL,
        )
        if acquired:
            return lock_value

        return None

    async def release_lock(
        self,
        key: str,
        lock_value: str,
    ) -> None:
        script = """
            if redis.call("get",KEYS[1])==ARGV[1] then
            redis.call("del",KEYS[1])
            return 1 
        end
        return 0
        """
        try:
            result = await self.redis.eval(
                script,
                1,
                key,
                lock_value,
            )
            logger.warning(
                "Redis lock was not released because ownership changed: %s",
                key,
            )
        except Exception:
            # IMPORTANT:
            # Lock cleanup failure should not hide the original
            # Groq/DB exception that caused us to enter finally.
            logger.exception(
                "Failed to release Redis lock: %s",
                key,
            )
