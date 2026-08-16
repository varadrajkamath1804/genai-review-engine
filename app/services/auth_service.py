from datetime import UTC, datetime, timedelta
from fastapi import Depends

from app.core.config import get_settings, Settings
from app.db.models.refresh_token import RefreshToken
from app.db.models.user import User
from app.models.user.user_login import UserLogin
from app.security.jwt import JWTManager
from app.exceptions.user import UserAlreadyExistsException, InvalidCredentialsException
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
        settings: Settings,
    ):
        self.user_repository = user_repository
        self.refresh_token_repository = refresh_token_repository
        self.settings = settings

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
        user = await self.user_repository.get_by_email(
            user_login.email,
        )

        if not user:
            raise InvalidCredentialsException()

        # user_login.password = "MyPassword123"
        # user.password      = "$2b$12$...."   ← bcrypt hash from DB

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
            + timedelta(days=self.settings.REFRESH_TOKEN_EXPIRE_DAYS),
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

        user_id = payload.get("sub")  # Used sub to store user_id while creating tokrn

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
            + timedelta(days=self.settings.REFRESH_TOKEN_EXPIRE_DAYS),
            created_at=datetime.now(UTC),
        )

        await self.refresh_token_repository.save(
            refresh_token_db,
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="Bearer",
        )

    async def logout(
        self,
        refresh_token: str,
    ) -> None:
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
