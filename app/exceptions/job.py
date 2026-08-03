from http import HTTPStatus
from app.exceptions.base import BaseAppException


class JobNotFoundException(BaseAppException):
    def __init__(self, job_id: str):
        super().__init__(
            status_code=HTTPStatus.NOT_FOUND,
            message=f"Job with ID {job_id} not found",
            error_code="JOB_NOT_FOUND",
        )


class JobProcessingException(BaseAppException):
    def __init__(self, message: str):
        super().__init__(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            message=f"Failed to prcess job:{message}",
            error_code="JOB_PROCESSING_ERROR",
        )


class JobNotCompletedException(BaseAppException):
    def __init__(self, job_id: str, current_status: str):
        super().__init__(
            status_code=HTTPStatus.BAD_REQUEST,
            message=f"Job {job_id} is not completed yet. Current status: {current_status}",
            error_code="JOB_NOT_COMPLETED",
        )
