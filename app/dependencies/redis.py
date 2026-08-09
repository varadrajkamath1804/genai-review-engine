from typing import Annotated

from fastapi import Depends, Request
from redis.asyncio import Redis
from app.services.cache_service import CacheService
from app.core.config import Settings, get_settings


def get_redis(request: Request) -> Redis:
    return request.app.state.redis


def get_cache_service(
    redis: Redis = Depends(get_redis),
    settings: Settings = Depends(get_settings),
) -> CacheService:

    return CacheService(
        redis=redis,
        settings=settings,
    )
