from http import HTTPStatus

from app.exceptions.base import BaseAppException


class DatabaseConnectionFailed(BaseAppException):
    def __init__(self):
        super().__init__(
            message="Database Connection Failed",
            error_code="DATABASE_CONNECTION_FAILED",
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
        )
