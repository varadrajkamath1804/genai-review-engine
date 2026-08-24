from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, Float, String
from pgvector.sqlalchemy import Vector

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.review_chunk import ReviewChunk


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    review: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    sentiment: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(384),
        nullable=True,
    )

    chunks: Mapped[list["ReviewChunk"]] = relationship(
        back_populates="review",
    )
