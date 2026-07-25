from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.db.models.review import Review
from app.models.query import SortOrder, SortField


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
        page: int,
        size: int,
        sentiment: str | None,
        review: str | None,
        sort_by: SortField,
        order: SortOrder,
    ) -> list[Review]:

        print("sort_by =", sort_by)
        print("order =", order)

        offset = (page - 1) * size
        query = select(Review)

        column = getattr(Review, sort_by.value)

        if sentiment is not None:
            query = query.where(Review.sentiment == sentiment)

        if review is not None:
            query = query.where(Review.review.ilike(f"%{review}%"))

        if order == SortOrder.desc:
            query = query.order_by(desc(column))
        else:
            query = query.order_by(column)

        query = query.limit(size).offset(offset)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(
        self,
        review_id: int,
    ) -> Review | None:
        result = await self.db.execute(select(Review).where(Review.id == review_id))
        return result.scalars().one_or_none()

    async def update(
        self,
        review: Review,
    ) -> Review:
        await self.db.commit()
        await self.db.refresh(review)
        return review
