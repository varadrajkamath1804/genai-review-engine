from fastapi import Depends

from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.services.auth_service import AuthService
from app.dependencies.repository import (
    get_user_repository,
    get_refresh_token_repository,
)


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
    refresh_token_repository: RefreshTokenRepository = Depends(
        get_refresh_token_repository
    ),
) -> AuthService:
    return AuthService(user_repository, refresh_token_repository)
