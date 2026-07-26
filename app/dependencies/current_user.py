from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.db.models.user import User
from app.dependencies.repository import get_user_repository
from app.exceptions.user import InvalidCredentialsException
from app.repositories.user_repository import UserRepository
from app.security.jwt import JWTManager

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login",
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(get_user_repository),
) -> User:
    """
    Verify JWT and return the authenticated user.
    """

    try:
        # Verify and decode JWT
        payload = JWTManager.decode_token(token)

        # Extract user id from JWT
        user_id = payload.get("sub")

        if user_id is None:
            raise InvalidCredentialsException()

    except JWTError:
        raise InvalidCredentialsException()

    # Find user in database
    user = await user_repository.get_by_id(
        int(user_id),
    )

    # User no longer exists
    if user is None:
        raise InvalidCredentialsException()

    return user
