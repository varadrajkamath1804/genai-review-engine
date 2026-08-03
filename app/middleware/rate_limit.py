import time
import logging
from typing import Dict, Optional, Tuple
from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.redis import get_redis
from app.exceptions import RateLimitExceededException

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.redis = None

    async def _get_redis(self):
        if self.redis is None:
            self.redis = await get_redis()
        return self.redis

    async def dispatch(self, request: Request, call_next):

        logger.info(f"RateLimitMiddleware: Processing {request.url.path}")

        # Step 1: Skip health checks
        if request.url.path in ["/health", "/db/health", "/db/redis/health"]:
            return await call_next(request)

        # Step 2: Get Redis client (raises exception if unavailable)
        redis = await self._get_redis()
        logger.info("RateLimitMiddleware: Redis connected")

        # Step 3: Get rate limit config for this endpoint
        limits = self._get_rate_limits(request.url.path, request.method)
        if not limits:
            return await call_next(request)

        # Step 4: Identify client
        client_ip = request.client.host if request.client else "unknown"
        key = f"ratelimit:{client_ip}:{request.url.path}"

        # Step 5: Check rate limit
        is_limited, remaining, reset_time = await self._check_rate_limit(
            redis=redis,
            key=key,
            max_requests=limits["max_requests"],
            window_seconds=limits["window_seconds"],
        )

        # Step 6: If limited, raise HTTPException (caught by global handler)
        if is_limited:
            logger.warning(f"Rate limit exceeded for {client_ip} on {request.url.path}")
            # raise RateLimitExceededException() Exception wont work in Middleware
            return Response(
                content='{"error":{"code":"RATE_LIMIT_EXCEEDED","message":"Too many requests. Try again later."}}',
                status_code=429,
                media_type="application/json",
                headers={
                    "X-RateLimit-Limit": str(limits["max_requests"]),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(reset_time),
                },
            )

        # Step 7: Process request
        response = await call_next(request)

        # Step 8: Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(limits["max_requests"])
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(reset_time)

        return response

    def _get_rate_limits(self, path: str, method: str) -> Optional[Dict]:
        """Define rate limits per endpoint."""

        # Auth endpoints (strict)
        if path == "/auth/login":
            return {"max_requests": 5, "window_seconds": 60}
        if path == "/auth/register":
            return {"max_requests": 3, "window_seconds": 3600}
        if path == "/auth/refresh":
            return {"max_requests": 10, "window_seconds": 60}

        # AI endpoints (cost control)
        if path.startswith("/ai/review"):
            return {"max_requests": 20, "window_seconds": 60}

        # Review endpoints (moderate)
        if path.startswith("/reviews"):
            if method == "POST":
                return {"max_requests": 30, "window_seconds": 60}
            return {"max_requests": 100, "window_seconds": 60}

        return None

    async def _check_rate_limit(
        self,
        redis,
        key: str,
        max_requests: int,
        window_seconds: int,
    ) -> Tuple[bool, int, int]:

        # Get Current Time
        now = int(time.time())

        # Calculate Window Start
        window_start = now - window_seconds

        # Remove Old Requests
        await redis.zremrangebyscore(key, 0, window_start)

        # Count Current Requests
        count = await redis.zcard(key)

        # Check if Limit Exceeded
        if count >= max_requests:
            # Get the oldest request in the window
            oldest = await redis.zrange(key, 0, 0, withscores=True)
            if oldest:
                oldest_time = oldest[0][1]  # Timestamp of oldest request
                reset_time = oldest_time + window_seconds
            else:
                reset_time = now + window_seconds
            return True, 0, reset_time

        # Add Current Request (If Allowed)
        await redis.zadd(key, {str(now): now})

        # Set Expiry
        await redis.expire(key, window_seconds)

        # Calculate Remaining Requests
        remaining = max_requests - count - 1

        # Calculate Reset Time (when the oldest request expires)
        oldest = await redis.zrange(key, 0, 0, withscores=True)
        if oldest:
            oldest_time = oldest[0][1]
            reset_time = oldest_time + window_seconds
        else:
            reset_time = now + window_seconds

        return False, remaining, reset_time
