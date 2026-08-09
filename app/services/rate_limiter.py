from redis.asyncio import Redis


class RateLimiter:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def is_allowed(
        self,
        key: str,
        limit: int,
        window: int,
    ) -> bool:
        count = await self.redis.incr(key)

        if count == 1:
            await self.redis.expire(key, window)

        return count <= limit
