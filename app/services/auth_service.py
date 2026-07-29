from datetime import UTC, datetime, timedelta

from app.core.config import get_settings
from app.db.models.refresh_token import RefreshToken
from app.db.models.user import User
from app.models.user.user_login import UserLogin
from app.security.jwt import JWTManager
from app.exceptions import (
    TokenExpiredException,
    TokenInvalidException,
    TokenRevokedException,
    UserAlreadyExistsException,
    InvalidCredentialsException,
)
from app.services.token_blacklist import TokenBlacklistService
from app.models.user.user_create import UserCreate
from app.models.user.user_response import UserResponse
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.security.hashing import PasswordHasher
from app.models.user.token_response import TokenResponse


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        refresh_token_repository: RefreshTokenRepository,
        blacklist_service: TokenBlacklistService,
    ):
        self.user_repository = user_repository
        self.refresh_token_repository = refresh_token_repository
        self.blacklist_service = blacklist_service

    async def signup(
        self,
        user: UserCreate,
    ) -> UserResponse:
        existing_user = await self.user_repository.get_by_email(
            user.email,
        )

        if existing_user:
            raise UserAlreadyExistsException(
                user.email,
            )

        hashed_password = PasswordHasher.hash_password(
            user.password,
        )

        new_user = User(
            name=user.name,
            email=user.email,
            password=hashed_password,
        )

        saved_user = await self.user_repository.save(
            new_user,
        )

        return UserResponse.model_validate(
            saved_user,
        )

    async def login(
        self,
        user_login: UserLogin,
    ) -> TokenResponse:
        """
        Authenticate a user and return a JWT.
        """
        settings = get_settings()

        user = await self.user_repository.get_by_email(
            user_login.email,
        )

        if not user:
            raise InvalidCredentialsException()

        if not PasswordHasher.verify_password(
            plain_password=user_login.password,
            hashed_password=user.password,
        ):
            raise InvalidCredentialsException()

        access_token = JWTManager.create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                "role": user.role.value,
                "type": "access",
            }
        )

        refresh_token = JWTManager.create_refresh_token(
            data={
                "sub": str(user.id),
                "type": "refresh",
            }
        )

        refresh_token_db = RefreshToken(
            user_id=user.id,
            token=refresh_token,
            expires_at=datetime.now(UTC)
            + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            created_at=datetime.now(UTC),
        )

        await self.refresh_token_repository.save(
            refresh_token_db,
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
        )

    async def refresh_token(
        self,
        refresh_token: str,
    ) -> TokenResponse:
        settings = get_settings()

        if await self.blacklist_service.is_blacklisted(refresh_token):
            raise TokenRevokedException()

        stored_token = await self.refresh_token_repository.get_by_token(
            refresh_token,
        )

        if stored_token is None:
            raise InvalidCredentialsException()

        await self.refresh_token_repository.delete(stored_token)

        payload = JWTManager.decode_token(
            refresh_token,
        )

        if payload.get("type") != "refresh":
            raise InvalidCredentialsException()

        user_id = payload.get("sub")

        if user_id is None:
            raise InvalidCredentialsException()

        user = await self.user_repository.get_by_id(
            int(user_id),
        )

        if user is None:
            raise InvalidCredentialsException()

        access_token = JWTManager.create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                "role": user.role.value,
                "type": "access_token",
            }
        )

        new_refresh_token = JWTManager.create_refresh_token(
            data={
                "sub": str(user.id),
                "type": "refresh",
            }
        )
        refresh_token_db = RefreshToken(
            user_id=user.id,
            token=new_refresh_token,
            expires_at=datetime.now(UTC)
            + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            created_at=datetime.now(UTC),
        )

        await self.refresh_token_repository.save(
            refresh_token_db,
        )

        await self.blacklist_service.add_to_blacklist(
            token=refresh_token,
            user_id=str(user.id),
            ttl=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="Bearer",
        )

    async def logout(
        self,
        refresh_token: str,
        user_id: int,
    ) -> None:

        settings = get_settings()
        await self.blacklist_service.add_to_blacklist(
            token=refresh_token,
            user_id=str(user_id),
            ttl=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        )

        stored_token = await self.refresh_token_repository.get_by_token(
            refresh_token,
        )

        if not stored_token:
            raise InvalidCredentialsException

        await self.refresh_token_repository.delete_by_token(
            refresh_token,
        )

    async def logout_all(
        self,
        user_id: int,
    ) -> None:
        await self.refresh_token_repository.delete_all_by_user_id(
            user_id,
        )
