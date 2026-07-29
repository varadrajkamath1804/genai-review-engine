import logging
from typing import Optional
from urllib.parse import quote_plus
from redis.asyncio import Redis
from app.core.config import get_settings

logger = logging.getLogger(__name__)

_redis_client: Optional[Redis] = None


async def get_redis() -> Redis:
    global _redis_client

    if _redis_client is None:
        settings = get_settings()

        password = settings.REDIS_PASSWORD
        if password and password.strip():
            # URL encode the password (handles @, #, !, etc.)
            encoded_password = quote_plus(password)
        if settings.REDIS_PASSWORD:
            url = f"redis://:{encoded_password}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
        else:
            url = f"redis://:{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"

        logger.info(
            f"Connecting to Redis at {settings.REDIS_HOST}:{settings.REDIS_PORT}"
        )

        _redis_client = Redis.from_url(
            url,
            decode_responses=True,
            protocol=2,
        )

        await _redis_client.ping()
        logger.info("Redis connected successfully")

    return _redis_client


async def close_redis() -> None:
    global _redis_client

    if _redis_client:
        await _redis_client.close()
        _redis_client = None
        logger.info("Redis connection closed")
