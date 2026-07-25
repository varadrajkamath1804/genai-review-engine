from http import HTTPStatus


class BaseAppException(Exception):
    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: HTTPStatus,
    ) -> None:
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(message)
