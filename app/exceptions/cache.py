from http import HTTPStatus

from app.exceptions.base import BaseAppException


class CacheLockException(BaseAppException):
    def __init__(self):
        super().__init__(
            message="Unable to acquire cache lock",
            error_code="CACHE_LOCK_FAILED",
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
        )
