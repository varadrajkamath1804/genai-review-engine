"""
Custom exceptions for the application.
"""

from app.exceptions.base import BaseAppException
from app.exceptions.user import (
    UserNotFoundException,
    UserAlreadyExistsException,
    InvalidCredentialsException,
    ForbiddenException,
)
from app.exceptions.review import (
    ReviewNotFoundException,
)
from app.exceptions.auth import (
    TokenExpiredException,
    TokenInvalidException,
    TokenRevokedException,
    TokenMissingException,
    RateLimitExceededException,
)
from app.exceptions.job import (
    JobNotCompletedException,
    JobProcessingException,
    JobNotFoundException,
)

__all__ = [
    # Base
    "BaseAppException",
    # User
    "UserNotFoundException",
    "UserAlreadyExistsException",
    "InvalidCredentialsException",
    "ForbiddenException",
    # Review
    "ReviewNotFoundException",
    # Auth (NEW)
    "TokenExpiredException",
    "TokenInvalidException",
    "TokenRevokedException",
    "TokenMissingException",
    "RateLimitExceededException",
    "JobNotCompletedException",
    "JobProcessingException",
    "JobNotFoundException",
]
