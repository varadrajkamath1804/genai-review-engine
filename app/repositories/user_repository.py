from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User


class UserRepository:
    """
    Handles all database operations related to users.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        # Database session injected by FastAPI
        self.db = db

    async def save(
        self,
        user: User,
    ) -> User:

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_by_email(
        self,
        email: str,
    ) -> User | None:

        statement = select(User).where(
            User.email == email,
        )
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_id(
        self,
        user_id: int,
    ) -> User | None:

        statement = select(User).where(
            User.id == user_id,
        )

        result = await self.db.execute(
            statement,
        )

        return result.scalar_one_or_none()
