from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.review import Review


class ReviewChunk(Base):
    __tablename__ = "review_chunks"

    # Primary key for each chunk.
    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    # Foreign key connecting this chunk to its original review.
    review_id: Mapped[int] = mapped_column(
        ForeignKey("reviews.id"),
        nullable=False,
    )

    # Relationship back to the parent Review.
    review: Mapped["Review"] = relationship(
        back_populates="chunks",
    )

    # The actual text content of this chunk.
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # Position of the chunk inside the original review.
    #
    # Example:
    # 0 = first chunk
    # 1 = second chunk
    # 2 = third chunk
    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # Vector embedding for THIS specific chunk.
    #
    # Your current embedding dimension is 384.
    embedding: Mapped[list[float]] = mapped_column(
        Vector(384),
        nullable=False,
    )

    # Additional information associated with the chunk.
    #
    # Example:
    # {
    #     "sentiment": "Negative",
    #     "confidence": 0.95
    # }
    metadata_: Mapped[dict] = mapped_column(
        "metadata",
        JSON,
        nullable=False,
    )
