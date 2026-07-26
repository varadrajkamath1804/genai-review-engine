from fastapi import Depends

from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.dependencies.repository import get_user_repository


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repository)
