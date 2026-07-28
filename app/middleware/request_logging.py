import logging
import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request: Request,
        call_next,
    ):
        start_time = time.perf_counter()

        # Reuse correlation ID if it already exists
        correlation_id = request.headers.get("X-Correlation-ID")

        if correlation_id is None:
            correlation_id = str(uuid.uuid4())

        # Every service generates its own request ID
        request_id = str(uuid.uuid4())

        # Store both IDs for the current request
        request.state.correlation_id = correlation_id
        request.state.request_id = request_id

        logger.info(
            "[Correlation: %s] [Request: %s] Incoming Request | %s %s",
            correlation_id,
            request_id,
            request.method,
            request.url.path,
        )

        response = await call_next(request)

        duration = (time.perf_counter() - start_time) * 1000

        logger.info(
            "[Correlation: %s] [Request: %s] Outgoing Response | %s %s | Status: %s | Duration: %.2f ms",
            correlation_id,
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

        response.headers["X-Correlation-ID"] = correlation_id
        response.headers["X-Request-ID"] = request_id

        return response
