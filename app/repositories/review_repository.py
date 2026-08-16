from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
import logging

from app.db.models.review import Review
from app.models.review.query import SortOrder, SortField

logger = logging.getLogger(__name__)


class ReviewRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(
        self,
        review: Review,
    ) -> Review:
        # Add the Review object to the current database session.
        self.db.add(review)

        # Persist the review and its embedding to PostgreSQL.
        await self.db.commit()

        # Refresh the object so it contains the latest database state.
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

        # Start building the SELECT query.
        query = select(Review)

        # Dynamically select the column used for sorting.
        column = getattr(Review, sort_by.value)

        # Filter by sentiment when provided.
        if sentiment is not None:
            query = query.where(Review.sentiment == sentiment)

        # Filter reviews using a case-insensitive text search.
        if review is not None:
            query = query.where(Review.review.ilike(f"%{review}%"))

        # Apply ascending or descending sorting.
        if order == SortOrder.desc:
            query = query.order_by(desc(column))
        else:
            query = query.order_by(column)

        # Apply pagination.
        query = query.limit(size).offset(offset)

        # Execute the query asynchronously.
        result = await self.db.execute(query)

        # Convert database rows into Review objects.
        return result.scalars().all()

    async def get_by_id(
        self,
        review_id: int,
    ) -> Review | None:

        # Find a single review using its primary key.
        result = await self.db.execute(select(Review).where(Review.id == review_id))

        return result.scalars().one_or_none()

    async def update(
        self,
        review: Review,
    ) -> Review:

        # The Review object has already been modified by the service.
        # Commit persists those changes, including a new embedding.
        await self.db.commit()

        # Refresh the object with the latest database state.
        await self.db.refresh(review)

        return review

    async def delete(
        self,
        review: Review,
    ) -> None:

        print("Deleting Review", review)

        # Remove the review from the database.
        await self.db.delete(review)

        # Persist the deletion.
        await self.db.commit()

    async def semantic_search(
        self,
        query_embedding: list[float],
        limit: int = 5,
        max_distance: float = 0.6,
    ) -> list[Review]:

        # Calculate cosine distance between the query embedding
        # and every stored review embedding.
        #
        # Smaller cosine distance = more semantically similar.

        # checks embedding of review with user given query (Review.embedding) with (query_embedding)
        distance = Review.embedding.cosine_distance(query_embedding)
        # print("Distance:", distance)

        # Ask PostgreSQL + pgvector to:
        # 1. Compare the query vector against stored vectors.
        # 2. Sort by similarity (smallest distance first).
        # 3. Return only the top `limit` results.
        query = (
            select(Review)
            .where(Review.embedding.is_not(None))
            # .where(distance <= max_distance)   kept of for now less data present in db
            .order_by(distance)
            .limit(limit)
        )

        # Execute the semantic-search query asynchronously.
        result = await self.db.execute(query)

        # Convert database rows into Review objects.
        return result.scalars().all()
