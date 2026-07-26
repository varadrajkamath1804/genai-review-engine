from app.db.models.user import User
from app.models.user.user_login import UserLogin
from app.security.jwt import JWTManager
from app.exceptions.user import UserAlreadyExistsException, InvalidCredentialsException
from app.models.user.user_create import UserCreate
from app.models.user.user_response import UserResponse
from app.repositories.user_repository import UserRepository
from app.security.hashing import PasswordHasher
from app.models.user.token_response import TokenResponse


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
    ):
        self.user_repository = user_repository

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
            }
        )

        return TokenResponse(
            access_token=access_token,
            token_type="Bearer",
        )
