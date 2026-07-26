from app.db.models.user import User
from app.exceptions.user import UserAlreadyExistsException
from app.models.user.user_create import UserCreate
from app.models.user.user_response import UserResponse
from app.repositories.user_repository import UserRepository
from app.security.hashing import PasswordHasher


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
