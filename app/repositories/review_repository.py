from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.review import Review


class ReviewRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(
        self,
        review: Review,
    ) -> Review:
        self.db.add(review)
        await self.db.commit()
        await self.db.refresh(review)
        return review

    async def get_all(
        self,
        page,
        size,
        sentiment,
    ) -> list[Review]:

        offset = (page - 1) * size
        query = select(Review)

        if sentiment is not None:
            query = query.where(Review.sentiment == sentiment)

        query = query.limit(size).offset(offset)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(
        self,
        review_id: int,
    ) -> Review | None:
        result = await self.db.execute(select(Review).where(Review.id == review_id))
        return result.scalars().one_or_none()
