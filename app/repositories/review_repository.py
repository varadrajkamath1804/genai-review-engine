from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.review import Review


class ReviewRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, review: Review) -> Review:
        self.db.add(review)
        await self.db.commit()
        await self.db.refresh(review)
        return review

    async def get_all(self) -> list[Review]:
        result = await self.db.execute(select(Review))
        return result.scalars().all()

    async def get_by_id(self, review_id: int) -> Review | None:
        result = await self.db.execute(select(Review).where(Review.id == review_id))
        return result.scalars().one_or_none()
