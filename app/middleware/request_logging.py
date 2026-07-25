import logging
import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        start_time = time.perf_counter()
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        logger.info(
            "[%s] Incoming Request | %s %s",
            request_id,
            request.method,
            request.url,
        )

        response = await call_next(request)

        duration = (time.perf_counter() - start_time) * 1000

        logger.info(
            "[%s] Outgoing Response | %s %s | Status: %s | Duration: %.2f ms",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

        return response
