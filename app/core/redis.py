from redis.asyncio import Redis
from app.core.config import get_settings


def create_redis_client() -> Redis:
    settings = get_settings()

    # DEBUG ONLY:
    # This tells us whether a password is being loaded,
    # without exposing the actual password.
    print("REDIS_HOST:", settings.REDIS_HOST)
    print("REDIS_PORT:", settings.REDIS_PORT)
    print("REDIS_DB:", settings.REDIS_DB)
    print("REDIS_PASSWORD SET:", bool(settings.REDIS_PASSWORD))

    return Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        # password=settings.REDIS_PASSWORD or None,
        password=None,
        decode_responses=True,
    )
