from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.refresh_token import RefreshToken


class RefreshTokenRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def save(
        self,
        refresh_token: RefreshToken,
    ) -> RefreshToken:
        self.db.add(refresh_token)
        await self.db.commit()
        await self.db.refresh(refresh_token)
        return refresh_token

    async def get_by_token(
        self,
        token: str,
    ) -> RefreshToken | None:
        statement = select(RefreshToken).where(
            RefreshToken.token == token,
        )
        result = await self.db.execute(statement)
        refresh_token = result.scalar_one_or_none()
        return refresh_token

    async def delete(
        self,
        refresh_token: RefreshToken,
    ) -> None:
        await self.db.delete(refresh_token)
        await self.db.commit()

    async def delete_by_token(
        self,
        token: str,
    ) -> None:
        statement = delete(RefreshToken).where(
            RefreshToken.token == token,
        )
        await self.db.execute(statement)
        await self.db.commit()

    async def delete_all_by_user_id(
        self,
        user_id: int,
    ) -> None:
        statement = delete(RefreshToken).where(
            RefreshToken.user_id == user_id,
        )
        await self.db.execute(statement)
        await self.db.commit()
