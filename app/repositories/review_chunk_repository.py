from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.review_chunk import ReviewChunk


class ReviewChunkRepository:
    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def save(self, review_chunk: ReviewChunk) -> ReviewChunk:
        self.db.add(review_chunk)
        await self.db.commit()
        await self.db.refresh(review_chunk)
        return review_chunk
