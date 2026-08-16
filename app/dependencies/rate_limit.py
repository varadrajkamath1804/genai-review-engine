from fastapi import Depends

from app.core.config import Settings, get_settings
from app.dependencies.redis import get_redis
from app.exceptions.rate_limit import RateLimitException
from app.services.rate_limiter import RateLimiter


async def rate_limit(
    settings: Settings = Depends(get_settings),
    redis=Depends(get_redis),
) -> None:

    print("🔥 RATE LIMIT STARTED")

    print("🔥 REDIS OBJECT:", redis)

    rate_limiter = RateLimiter(redis)

    print("🔥 CALLING REDIS INCR")

    allowed = await rate_limiter.is_allowed(
        key="rate:global",
        limit=settings.REDIS_RATE_LIMIT,
        window=settings.REDIS_RATE_WINDOW,
    )

    print(f"🔥 RATE LIMIT RESULT: {allowed}")

    if not allowed:
        raise RateLimitException()
