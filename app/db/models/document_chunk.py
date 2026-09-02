from datetime import datetime
from typing import Any

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class DocumentChunk(Base):
    """
    Represents one retrieval-friendly chunk
    extracted from an uploaded document.
    """

    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
    )

    context: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    meta_data: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
    )

    # all-MiniLM-L6-v2 produces 384 dimensions.
    embedding = mapped_column(
        Vector(384),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # Many chunks belong to one document.
    document = relationship(
        "Document",
        back_populates="chunks",
    )
