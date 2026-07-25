from http import HTTPStatus

from app.exceptions.base import BaseAppException


class ReviewNotFoundException(BaseAppException):
    def __init__(self, review_id: int):
        super().__init__(
            message=f"Review with id {review_id} not found",
            error_code="REVIEW NOT FOUND",
            status_code=HTTPStatus.NOT_FOUND,
        )
