"""
Authentication-related exceptions.
"""

from http import HTTPStatus
from app.exceptions.base import BaseAppException


class TokenExpiredException(BaseAppException):
    """Raised when a token has expired."""

    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.UNAUTHORIZED,
            error_code="TOKEN_EXPIRED",
            message="Token has expired. Please login again.",
        )


class TokenInvalidException(BaseAppException):
    """Raised when a token is invalid."""

    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.UNAUTHORIZED,
            error_code="TOKEN_INVALID",
            message="Invalid token. Please login again.",
        )


class TokenRevokedException(BaseAppException):
    """Raised when a token has been revoked (blacklisted)."""

    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.UNAUTHORIZED,
            error_code="TOKEN_REVOKED",
            message="Token has been revoked. Please login again.",
        )


class TokenMissingException(BaseAppException):
    """Raised when a token is missing from request."""

    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.UNAUTHORIZED,
            error_code="TOKEN_MISSING",
            message="Authentication token is missing.",
        )


class RateLimitExceededException(BaseAppException):
    """Raised when Rate limit exceeded"""

    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.TOO_MANY_REQUESTS,
            error_code="RATE_LIMIT_EXCEEDED",
            message="Too many requests. Try again later.",
        )
