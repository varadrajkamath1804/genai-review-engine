from http import HTTPStatus

from app.exceptions.base import BaseAppException


class RateLimitException(BaseAppException):
    def __init__(self):
        super().__init__(
            message="Rate limit exceeded",
            error_code="RATE_LIMIT_EXCEEDED",
            status_code=HTTPStatus.TOO_MANY_REQUESTS,
        )
