import asyncio

from app.core.redis import create_redis_client


async def main():
    redis = create_redis_client()

    try:
        response = await redis.ping()
        print(f"Redis response: {response}")
    finally:
        await redis.aclose()


asyncio.run(main())
