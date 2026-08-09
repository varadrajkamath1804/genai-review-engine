from redis.asyncio import Redis
from app.core.config import get_settings


def create_redis_client() -> Redis:
    settings = get_settings()

    return Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD or None,
        decode_responses=True,
    )
