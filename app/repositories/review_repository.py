from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.review import Review


class ReviewRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, review: Review) -> Review:
        self.db.add(review)
        await self.db.commit()
        await self.db.refresh(review)
        return review
