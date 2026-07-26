from http import HTTPStatus

from app.exceptions.base import BaseAppException


class UserNotFoundException(BaseAppException):
    def __init__(self, user_email: str):
        super().__init__(
            message=f"User with email {user_email} not found",
            error_code="USER NOT FOUND",
            status_code=HTTPStatus.NOT_FOUND,
        )


class UserAlreadyExistsException(BaseAppException):
    def __init__(self, user_email: str):
        super().__init__(
            message=f"User with email {user_email} already exists",
            error_code="USER ALREADY EXISTS",
            status_code=HTTPStatus.CONFLICT,
        )


class InvalidcredentialException(BaseAppException):
    def __init__(self):
        super().__init__(
            message="Invalid Email or Password",
            error_code="INVALID CREDENTIALS",
            status_code=HTTPStatus.UNAUTHORIZED,
        )
