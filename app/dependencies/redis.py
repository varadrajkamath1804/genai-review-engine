from redis.asyncio import Redis
from app.core.redis import get_redis


async def get_redis_client() -> Redis:
    return await get_redis()
