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
    "ReviewPermissionDeniedException",
    # Auth (NEW)
    "TokenExpiredException",
    "TokenInvalidException",
    "TokenRevokedException",
    "TokenMissingException",
]
